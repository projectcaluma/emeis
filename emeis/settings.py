import os
import re
from warnings import warn

import environ
from django.conf import global_settings
from pkg_resources import resource_filename

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Application definition

INSTALLED_APPS = [
    "django.contrib.postgres",
    "localized_fields",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "mozilla_django_oidc",
    "mptt",
    "generic_permissions.apps.GenericPermissionsConfig",
    "emeis.core.apps.DefaultConfig",
]

if ENV == "dev":
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "emeis.urls"
WSGI_APPLICATION = "emeis.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.str("DATABASE_NAME", default="emeis"),
        "USER": env.str("DATABASE_USER", default="emeis"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("emeis")),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default={}),
    }
}


# Cache
# https://docs.djangoproject.com/en/1.11/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": env.str(
            "CACHE_BACKEND", default="django.core.cache.backends.locmem.LocMemCache"
        ),
        "LOCATION": env.str("CACHE_LOCATION", ""),
    }
}


# Extensions

EMEIS_VISIBILITY_CLASSES = env.list(
    "EMEIS_VISIBILITY_CLASSES", default=(["generic_permissions.visibilities.Any"])
)

EMEIS_PERMISSION_CLASSES = env.list(
    "EMEIS_PERMISSION_CLASSES", default=(["generic_permissions.permissions.AllowAny"])
)

VISIBILITY_CLASSES = env.list(
    "VISIBILITY_CLASSES", default=default(["generic_permissions.visibilities.Any"])
)

PERMISSION_CLASSES = env.list(
    "PERMISSION_CLASSES", default=default(["generic_permissions.permissions.AllowAny"])
)

# Reading PERMISSION_CLASSES, VISIBILITY_CLASSES is still supported. If
# it's set but EMEIS_* is not, copy over the config
if PERMISSION_CLASSES and not EMEIS_PERMISSION_CLASSES:  # pragma: no cover
    EMEIS_PERMISSION_CLASSES = PERMISSION_CLASSES
if VISIBILITY_CLASSES and not EMEIS_VISIBILITY_CLASSES:  # pragma: no cover
    EMEIS_VISIBILITY_CLASSES = VISIBILITY_CLASSES


# VISIBILITY_CLASSES and PERMISSION_CLASSES are deprecated, but
# still supported for now. If they're set, notify the user.
def _deprecate_env(name, replacement):
    if env.str(name, default=False):  # pragma: no cover
        warn(
            DeprecationWarning(
                f"The {name} setting is deprecated and will be removed "
                f"in a future version of Emeis. Use {replacement}"
            )
        )


_deprecate_env("PERMISSION_CLASSES", "EMEIS_PERMISSION_CLASSES")
_deprecate_env("VISIBILITY_CLASSES", "EMEIS_VISIBILITY_CLASSES")


EMEIS_VALIDATION_CLASSES = env.list("EMEIS_VALIDATION_CLASSES", default=[])

# We use DGAP as a permission/visibility/validation handler. Copy
# the configuration over so DGAP knows
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = EMEIS_VISIBILITY_CLASSES
GENERIC_PERMISSIONS_PERMISSION_CLASSES = EMEIS_PERMISSION_CLASSES
GENERIC_PERMISSIONS_VALIDATION_CLASSES = EMEIS_VALIDATION_CLASSES

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


def parse_languages(languages):
    return [(language, language) for language in languages]


LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en")
LANGUAGES = (
    parse_languages(env.list("LANGUAGES", default=["en"])) or global_settings.LANGUAGES
)
LOCALE_PATHS = env.list("LOCALE_PATHS", default=[django_root("emeis", "locale")])

TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Authentication
AUTH_USER_MODEL = "emeis_core.User"

OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT", default=None)
OIDC_OP_TOKEN_ENDPOINT = "not supported in emeis, but a value is needed"
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_USERNAME_CLAIM = env.str("OIDC_USERNAME_CLAIM", default="sub")
OIDC_EMAIL_CLAIM = env.str("OIDC_EMAIL_CLAIM", default="email")
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)
OIDC_CREATE_USER = env.bool("OIDC_CREATE_USER", False)
OIDC_UPDATE_USER = env.bool("OIDC_UPDATE_USER", False)
OIDC_OP_INTROSPECT_ENDPOINT = env.str("OIDC_OP_INTROSPECT_ENDPOINT", default=None)
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID", default=None)
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET", default=None)
OIDC_DRF_AUTH_BACKEND = "emeis.oidc_auth.authentication.EmeisAuthenticationBackend"

EMEIS_OIDC_USER_FACTORY = env.str(
    "EMEIS_OIDC_USER_FACTORY", default="emeis.oidc_auth.authentication.OIDCUser"
)

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "emeis.core.filters.CaseInsensitiveOrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "SEARCH_PARAM": "filter[search]",
    "ORDERING_PARAM": "sort",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True


# Anonymous writing
ALLOW_ANONYMOUS_WRITE = env.bool("ALLOW_ANONYMOUS_WRITE", default=False)

if ALLOW_ANONYMOUS_WRITE:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny",
    ]


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("ADMINS", default=[]))

USER_EXPORT_TEMPLATE_PATH = env.str(
    "USER_EXPORT_TEMPLATE_PATH",
    default=resource_filename("emeis.core", "templates/user_list.xlsx"),
)

# Cors headers
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["console"], "level": env.str("LOG_LEVEL", default="INFO")}
    },
}
