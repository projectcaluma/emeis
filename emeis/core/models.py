import unicodedata
import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework import exceptions


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


class VisibilityMixin:
    visibility_classes = None

    @classmethod
    def visibility_queryset_filter(cls, queryset, request, **kwargs):
        if cls.visibility_classes is None:
            raise ImproperlyConfigured(
                "check that app `emeis.core.DefaultConfig` is part of your `INSTALLED_APPS`."
            )

        for visibility_class in cls.visibility_classes:
            queryset = visibility_class().filter_queryset(cls, queryset, request)

        return queryset


class PermissionMixin:
    permission_classes = None

    @classmethod
    def check_permissions(cls, request, **kwargs):
        if cls.permission_classes is None:
            raise ImproperlyConfigured(
                "check that app `emeis.core.DefaultConfig` is part of your `INSTALLED_APPS`."
            )

        for permission_class in cls.permission_classes:
            if not permission_class().has_permission(cls, request):
                raise exceptions.PermissionDenied()

    def check_object_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_object_permission(
                self.__class__, request, self
            ):
                raise exceptions.PermissionDenied()


class BaseModel(VisibilityMixin, PermissionMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by_user = models.ForeignKey("User", null=True, on_delete=models.SET_NULL)
    meta = JSONField(_("meta"), default=dict)

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


class User(UUIDModel):
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

    def __str__(self):
        return "%s object (%s - %s)" % (self.__class__.__name__, self.pk, self.username)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

        self.email = BaseUserManager.normalize_email(self.email)

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


class Scope(MPTTModel, UUIDModel):
    name = LocalizedCharField(_("scope name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("scope description"), null=True, blank=True, required=False
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )


class Role(SlugModel):
    name = LocalizedCharField(_("role name"), blank=False, null=False, required=False)
    description = LocalizedTextField(
        _("role description"), null=True, blank=True, required=False
    )
    permissions = models.ManyToManyField("Permission", related_name="roles")

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
        return "%s object (%s - %s - %s)" % (
            self.__class__.__name__,
            self.user.username,
            self.scope,
            self.role,
        )

    class Meta:
        unique_together = ["user", "scope", "role"]
