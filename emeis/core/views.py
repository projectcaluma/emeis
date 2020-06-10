from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import models, serializers


class BaseViewset(views.ModelViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.model.visibility_queryset_filter(queryset, self.request)


class MeViewSet(RetrieveModelMixin, GenericViewSet):
    """Me view returns current user."""

    serializer_class = serializers.MeSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user


class MyACLViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """MyACL view returns current users ACLs."""

    queryset = models.ACL.objects.all()
    serializer_class = serializers.MyACLSerializer

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


class ScopeViewSet(BaseViewset):
    serializer_class = serializers.ScopeSerializer
    queryset = models.Scope.objects.all()


class RoleViewSet(BaseViewset):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()


class PermissionViewSet(BaseViewset):
    serializer_class = serializers.PermissionSerializer
    queryset = models.Permission.objects.all()


class ACLViewSet(BaseViewset):
    serializer_class = serializers.ACLSerializer
    queryset = models.ACL.objects.all()
