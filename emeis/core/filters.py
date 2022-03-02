from django.conf import settings
from django.db.models.functions import Lower
from django_filters import FilterSet
from django_filters.filters import CharFilter
from rest_framework import filters

from emeis.core.models import User


class MonolingualSearchFilter(filters.SearchFilter):

    multilingual_search_fields = []

    def get_search_fields(self, view, request):
        """Return search fields for the current view.

        The search fields are defined on the viewset as normal, but if the
        model is configured as a "forced monolingual" model, we use the default
        language instead for searching.

        """

        model_name = view.queryset.model.__name__.lower()

        if model_name not in settings.EMEIS_FORCE_MODEL_LOCALE:
            return super().get_search_fields(view, request)

        forced_lang = settings.EMEIS_FORCE_MODEL_LOCALE[model_name]

        return [
            f"{field}__{forced_lang}"
            if field in view.multilingual_search_fields
            else field
            for field in view.search_fields
        ]


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
        }


class CaseInsensitiveOrderingFilter(filters.OrderingFilter):
    def _make_ordering_field(self, field, view):
        desc = field.startswith("-")
        field_name = field[1:] if desc else field

        if field_name in getattr(view, "case_insensitive_ordering_fields", []):
            return Lower(field_name).desc() if desc else Lower(field_name)
        return field

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if not ordering:
            return ordering
        return [self._make_ordering_field(field, view) for field in ordering]
