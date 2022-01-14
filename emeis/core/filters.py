from django.db.models.functions import Lower
from django_filters import FilterSet
from django_filters.filters import CharFilter
from rest_framework import filters

from emeis.core.models import User


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
    def get_ordering(self, request, queryset, view):
        case_insensitive_fields = getattr(view, "case_insensitive_ordering_fields", [])
        ordering = super().get_ordering(request, queryset, view)
        if not ordering:
            return ordering
        return [(Lower(o) if o in case_insensitive_fields else o) for o in ordering]
