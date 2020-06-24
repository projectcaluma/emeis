from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers


class BaseViewset(views.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.model.visibility_queryset_filter(queryset, self.request)

    def destroy(self, request, *args, **kwargs):
        self.queryset.model.check_permissions(request)
        instance = self.get_object()
        instance.check_object_permissions(request)
        # we do not call `super()` in order to not fetch the object twice.
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class MeViewSet(RetrieveModelMixin, GenericViewSet):
    """Me view returns current user."""

    serializer_class = serializers.MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return self.request.user


class MyACLViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """MyACL view returns current users ACLs."""

    queryset = models.ACL.objects.all()
    serializer_class = serializers.MyACLSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.pop("pk")
        acl = get_object_or_404(models.ACL, pk=pk)
        if acl.user != self.request.user:
            raise PermissionDenied()
        return acl

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserViewSet(BaseViewset):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "=zip",
        "city",
    )


class ScopeViewSet(BaseViewset):
    serializer_class = serializers.ScopeSerializer
    queryset = models.Scope.objects.all()
    search_fields = (
        "name",
        "description",
    )


class RoleViewSet(BaseViewset):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()
    search_fields = (
        "slug",
        "name",
        "description",
    )


class PermissionViewSet(BaseViewset):
    serializer_class = serializers.PermissionSerializer
    queryset = models.Permission.objects.prefetch_related("roles")
    filterset_fields = ("roles",)
    search_fields = (
        "slug",
        "name",
        "description",
    )


class ACLViewSet(BaseViewset):
    serializer_class = serializers.ACLSerializer
    queryset = models.ACL.objects.all()
    filterset_fields = ("user", "scope", "role")
    search_fields = (
        "scope__name",
        "scope__description",
        "role__name",
        "role__description",
        "user__username",
        "user__first_name",
        "user__last_name",
        "=user__zip",
        "user__city",
    )
