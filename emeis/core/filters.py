from django_filters import FilterSet
from django_filters.filters import CharFilter

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
