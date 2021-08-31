from django.contrib.auth.models import AnonymousUser
from generic_permissions.visibilities import filter_queryset_for

from . import models


class OwnAndAdmin:
    """Example permissions class, allowing to see only own objects, unless user is admin.

    Note: This assumes that there is a role named "admin". Once the user has
    that role on any scope, they are assumed to be an admin.

    You can sublcass this and implement your own is_admin() method if your
    logic differs.
    """

    def generic_own_and_admin(
        self, request, queryset, _filters_cb=lambda: {}, none=False
    ):
        if isinstance(request.user, AnonymousUser):
            return queryset.none()
        elif self.is_admin(request.user):
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

    def is_admin(self, user):
        """Return True if given OIDC user is admin.

        Sublcass OwnAndAdmin and overload this method
        to implement your own logic.
        """
        return user.user.acls.filter(role_id="admin").exists()
