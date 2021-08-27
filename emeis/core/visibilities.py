from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from generic_permissions.visibilities import filter_queryset_for

from . import models


class OwnAndAdmin:
    @staticmethod
    def generic_own_and_admin(request, queryset, _filters_cb=lambda: {}, none=False):
        if isinstance(request.user, AnonymousUser):
            return queryset.none()
        elif request.user.username == settings.ADMIN_USERNAME:
            return queryset
        if none:
            return queryset.none()
        return queryset.filter(**_filters_cb())

    @filter_queryset_for(models.User)
    def filter_queryset_for_user(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"pk": request.user.user.pk}
        )

    @filter_queryset_for(models.Scope)
    @filter_queryset_for(models.Role)
    def filter_queryset_for_scope_and_role(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"acls__user": request.user.user.pk}
        )

    @filter_queryset_for(models.Permission)
    def filter_queryset_for_permission(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"roles__acls__user": request.user.user.pk}
        )

    @filter_queryset_for(models.ACL)
    def filter_queryset_for_acl(self, queryset, request):
        return self.generic_own_and_admin(request, queryset, none=True)
