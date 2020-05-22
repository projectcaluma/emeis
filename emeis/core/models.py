import unicodedata
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by_user = models.ForeignKey("User", null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class UUIDModel(BaseModel):
    """
    Models which use uuid as primary key.

    Defined as emeis default
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    phone = models.CharField(_("phone"), max_length=100, blank=True, null=True)
    language = models.CharField(_("language"), max_length=2)
    address = models.CharField(_("address"), max_length=255, blank=True, null=True)
    city = models.CharField(_("city"), max_length=255, blank=True, null=True)
    zip = models.CharField(_("zip"), max_length=10, blank=True, null=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    meta = JSONField(_("meta"), default=dict)

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
