import unicodedata
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Exists, OuterRef, Q, Subquery
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField


def make_uuid():
    """Return a new random UUID value.

    This indirection is done for testing purposes, so test code can mock
    uuid.uuid4(). If we wouldn't do this, then the models would have a direct
    reference that doesn't get mocked away.

    We can't replace it with a lambda because Django Migrations can't handle them.
    """
    return uuid.uuid4()


def get_language_code():
    return settings.LANGUAGE_CODE


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by_user = models.ForeignKey(
        "User", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    metainfo = models.JSONField(_("metainfo"), default=dict)

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    """
    Models which use uuid as primary key.

    Defined as emeis default
    """

    id = models.UUIDField(primary_key=True, default=make_uuid, editable=False)

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    """
    Models which use a slug as primary key.

    Defined as Emeis default for configuration so it is possible
    to merge between developer and user configuration.
    """

    slug = models.SlugField(max_length=255, primary_key=True)

    class Meta:
        abstract = True


class User(UUIDModel, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=255,
        unique=True,
        help_text=_(
            "Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    first_name = models.CharField(
        _("first name"), max_length=255, blank=True, null=True
    )
    last_name = models.CharField(_("last name"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    phone = models.CharField(_("phone"), max_length=100, blank=True, null=True)
    language = models.CharField(_("language"), max_length=2, default=get_language_code)
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    city = LocalizedCharField(_("city"), max_length=255, blank=True, null=True)
    zip = models.CharField(_("zip"), max_length=10, blank=True, null=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return "%s (username=%s)" % (type(self).__name__, self.username)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

        self.email = UserManager.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def natural_key(self):
        return self.get_username()

    @classmethod
    def get_email_field_name(cls):
        return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )

    @property
    def is_anonymous(self):
        """
        Return False.

        This is a way of comparing User objects to anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Return True.

        This is a way to tell if the user has been authenticated in templates.
        """
        return True


class ScopeQuerySet(models.QuerySet):
    def all_descendants(self, include_self=False):
        """Return a QS that contains all descendants."""
        expr = Q(all_parents__overlap=self.aggregate(all_pks=ArrayAgg("pk"))["all_pks"])

        if include_self:
            expr = expr | Q(pk__in=self)

        return Scope.objects.filter(expr)

    def all_ancestors(self, include_self=False):
        """Return a QS that contains all ancestors."""

        filter_qs = self.filter(all_parents__contains=[OuterRef("pk")])

        new_qs = Scope.objects.all().annotate(_is_ancestor=Exists(Subquery(filter_qs)))
        expr = Q(_is_ancestor=True)

        if include_self:
            expr = expr | Q(pk__in=self)

        return new_qs.filter(expr)

    def all_roots(self):
        return self.all_ancestors(include_self=True).filter(parent__isnull=True)


class Scope(UUIDModel):
    name = LocalizedCharField(_("scope name"), blank=False, null=False, required=False)

    full_name = LocalizedCharField(
        _("scope name"), blank=True, null=True, required=False
    )

    description = LocalizedTextField(
        _("scope description"), null=True, blank=True, required=False
    )
    is_active = models.BooleanField(default=True)

    objects = ScopeQuerySet.as_manager()

    parent = models.ForeignKey(
        "Scope",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    all_parents = ArrayField(models.UUIDField(null=False), default=list)

    def ancestors(self, include_self=False):
        expr = Q(pk__in=self.all_parents)
        if include_self:
            expr = expr | Q(pk=self.pk)
        return Scope.objects.all().filter(expr)

    def descendants(self, include_self=False):
        expr = Q(all_parents__contains=[self.pk])

        if include_self:
            expr = expr | Q(pk=self.pk)

        return Scope.objects.all().filter(expr)

    def get_root(self):
        if self.parent_id:
            return Scope.objects.get(pk=self.all_parents[0])
        else:
            return self

    def save(self, *args, **kwargs):
        self._ensure_no_loop()
        return super().save(*args, **kwargs)

    def _ensure_no_loop(self):
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError(
                    "A node cannot be made a descendant or parent of itself"
                )
            parent = parent.parent

    def __str__(self):
        return f"{type(self).__name__} ({self.full_name}, pk={self.pk})"

    class Meta:
        ordering = ["name"]
        indexes = [GinIndex(fields=["all_parents"])]


@receiver(pre_save, sender=Scope)
def set_full_name_and_parents(instance, sender, **kwargs):
    """Update the `full_name` and `all_parents` properties of the Scope.

    The full name depends on the complete list of parents of the Scope.
    And to ensure correct behaviour in the queries, the `all_parents`
    attribute needs to be updated as well
    """
    if kwargs.get("raw"):  # pragma: no cover
        # Raw is set while loading fixtures. In those
        # cases we don't want to mess with data that
        # may not be there yet
        return
    sep = "\u00bb"

    languages = [lang for lang, _ in settings.LANGUAGES]

    forced_lang = settings.EMEIS_FORCE_MODEL_LOCALE.get("scope", None)

    old_all_parents = [*instance.all_parents]
    old_full_name = {**instance.full_name}

    if forced_lang:
        # If scope is forced monolingual, do not fill non-forced language fields
        languages = [forced_lang]

    for lang in languages:
        with translation.override(lang):
            instance.full_name[lang] = str(instance.name)

    parent_ids = []
    parent = instance.parent
    while parent:
        parent_ids.append(parent.pk)
        for lang in languages:
            with translation.override(lang):
                new_fullname = f"{parent.name} {sep} {instance.full_name[lang]}"
                instance.full_name[lang] = new_fullname
        parent = parent.parent

    # make it root-first
    parent_ids.reverse()
    instance.all_parents = parent_ids

    if forced_lang:
        # Ensure only the "forced" language full_name is set, and nothing else
        full_name = instance.full_name[forced_lang]
        instance.full_name.clear()
        instance.full_name[forced_lang] = full_name

    if old_all_parents != instance.all_parents or old_full_name != dict(
        instance.full_name
    ):
        # Something changed - force update all children (recursively)
        for child in instance.children.all():
            # save() triggers the signal handler, which will
            # recurse all the way down, updating the full_name
            child.save()


class Role(SlugModel):
    name = LocalizedCharField(_("role name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("role description"), null=True, blank=True, required=False
    )
    permissions = models.ManyToManyField("Permission", related_name="roles")

    def __str__(self):
        return f"{type(self).__name__} ({self.pk})"

    class Meta:
        ordering = ["slug"]


class Permission(SlugModel):
    name = LocalizedCharField(
        _("permission name"), blank=False, null=False, required=False
    )
    description = LocalizedTextField(
        _("permission description"), null=True, blank=True, required=False
    )


class ACL(UUIDModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="acls")
    scope = models.ForeignKey("Scope", on_delete=models.CASCADE, related_name="acls")
    role = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="acls")

    def __str__(self):
        return f"{type(self).__name__} (username={self.user.username}, scope=self.scope, role={self.role.pk})"

    class Meta:
        unique_together = ["user", "scope", "role"]
