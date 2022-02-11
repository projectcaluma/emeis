import io
from tempfile import NamedTemporaryFile

import openpyxl
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from generic_permissions.permissions import PermissionViewMixin
from generic_permissions.visibilities import VisibilityViewMixin
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api import views

from . import filters, models, serializers


class BaseViewset(VisibilityViewMixin, PermissionViewMixin, views.ModelViewSet):
    pass


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

    filterset_class = filters.UserFilterset

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "=zip",
        "city",
    )

    case_insensitive_ordering_fields = [
        "first_name",
        "last_name",
        "email",
        "address",
        "city",
    ]

    @action(methods=["get"], detail=False)
    def export(self, request):
        """Export user list as excel table."""
        queryset = self.get_queryset()

        # we use a template to set the headers to bold and align the columns to fit on a DIN-A4 page
        workbook = openpyxl.load_workbook(settings.USER_EXPORT_TEMPLATE_PATH)
        sheet = workbook.active

        # set column headers
        sheet["A1"] = _("Name")
        sheet["B1"] = _("First Name")
        sheet["C1"] = _("Email")
        sheet["D1"] = _("Roles and organizations")

        for row, user in enumerate(queryset.iterator(), start=2):
            acl_string = "\n".join(
                [
                    f"{acl.role.name}: {acl.scope.full_name()}"
                    for acl in user.acls.all()
                    .select_related("scope", "role")
                    .order_by("role__name")
                ]
            )

            sheet[f"A{row}"] = user.last_name
            sheet[f"B{row}"] = user.first_name
            sheet[f"C{row}"] = user.email
            sheet[f"D{row}"] = acl_string
            sheet[f"D{row}"].alignment = openpyxl.styles.Alignment(wrap_text=True)

        # save workbook as temporary file and read the file
        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            tmp.seek(0)
            binary_data = tmp.read()
            workbook.close()
            tmp.close()

        return FileResponse(
            io.BytesIO(binary_data),
            as_attachment=True,
            filename="export.xlsx",
        )


class ScopeViewSet(BaseViewset):
    serializer_class = serializers.ScopeSerializer
    queryset = models.Scope.objects.all()
    search_fields = (
        "name",
        "description",
    )
    case_insensitive_ordering_fields = [
        "name",
        "description",
    ]


class RoleViewSet(BaseViewset):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()
    search_fields = (
        "slug",
        "name",
        "description",
    )
    case_insensitive_ordering_fields = [
        "name",
        "description",
    ]


class PermissionViewSet(BaseViewset):
    serializer_class = serializers.PermissionSerializer
    queryset = models.Permission.objects.prefetch_related("roles")
    filterset_fields = ("roles",)
    search_fields = (
        "slug",
        "name",
        "description",
    )
    case_insensitive_ordering_fields = [
        "name",
        "description",
    ]


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
