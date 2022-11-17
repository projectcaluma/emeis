from django.conf import settings
from django.contrib.postgres.fields.hstore import KeyTransform
from django.core.exceptions import FieldDoesNotExist
from django.db.models import TextField
from django.db.models.functions import Cast, Lower
from django_filters import FilterSet
from django_filters.filters import CharFilter
from localized_fields.fields import LocalizedField
from rest_framework import filters

from emeis.core import utils
from emeis.core.models import ACL, Scope, User


class EmeisSearchFilter(filters.SearchFilter):
    """Custom search filter for Emeis.

    This adds two things:
    - "monolingual" search support via EMEIS_FORCE_MODEL_LOCALE
    - search support for EMEIS_META_FIELDS
    """

    multilingual_search_fields = []

    def get_search_fields(self, view, request):
        """Return search fields for the current view.

        The search fields are defined on the viewset as normal, but if the
        model is configured as a "forced monolingual" model, we use the default
        language instead for searching.

        """

        model_name = view.queryset.model.__name__.lower()

        meta_fields = [f"metainfo__{f}" for f in settings.EMEIS_META_FIELDS]

        if model_name not in settings.EMEIS_FORCE_MODEL_LOCALE:
            default_fields = super().get_search_fields(view, request)
            return list(default_fields) + meta_fields if default_fields else meta_fields

        forced_lang = settings.EMEIS_FORCE_MODEL_LOCALE[model_name]

        return [
            f"{field}__{forced_lang}"
            if field in view.multilingual_search_fields
            else field
            for field in view.search_fields
        ] + meta_fields


class UserFilterset(FilterSet):
    has_role = CharFilter(
        field_name="acls__role__pk",
        distinct=True,
    )

    class Meta:
        model = User

        fields = {
            "id": ["exact", "in"],
            "username": ["exact", "in"],
            "first_name": ["exact", "icontains", "contains"],
            "last_name": ["exact", "icontains", "contains"],
            "email": ["exact", "in"],
            "is_active": ["exact"],
        }


class ACLFilterset(FilterSet):
    class Meta:
        model = ACL
        fields = {
            "id": ["exact", "in"],
            "user": ["exact", "in"],
            "scope": ["exact", "in"],
            "role": ["exact", "in"],
        }


class EmeisOrderingFilter(filters.OrderingFilter):
    """Custom ordering filter for Emeis.

    This adds two things:
    - case insensitive ordering via "case_insensitive_ordering_fields"
    - ordering by metainfo fields
    """

    def get_valid_fields(self, queryset, view, context=None):
        ordering_fields = super().get_valid_fields(queryset, view, context or {})
        return ordering_fields + [
            (f"metainfo__{field}", f"{field} in metainfo")
            for field in settings.EMEIS_META_FIELDS
        ]

    def _make_ordering_field(self, field, view):
        model_name = view.queryset.model.__name__
        lang = utils.forced_or_current_lang(model_name)

        desc = field.startswith("-")
        field_name = field[1:] if desc else field

        field_col = field_name
        try:
            model_field = view.queryset.model._meta.get_field(field_name)
            if isinstance(model_field, LocalizedField):

                field_col = KeyTransform(lang, field_name)
        except FieldDoesNotExist:
            # This happens with metainfo__foobar style lookups,
            # which we don't need to worry about here
            pass

        if field_name in self._get_case_insensitive_fields(view):
            field_expr = Lower(Cast(field_col, output_field=TextField()))
            return field_expr.desc() if desc else field_expr
        return field

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if not ordering:
            return ordering
        return [self._make_ordering_field(field, view) for field in ordering]

    def _get_case_insensitive_fields(self, view):
        return getattr(view, "case_insensitive_ordering_fields", []) + [
            f"metainfo__{field}" for field in settings.EMEIS_META_FIELDS
        ]


class ScopeFilterset(FilterSet):
    class Meta:
        model = Scope
        fields = {
            "id": ["exact", "in"],
        }
