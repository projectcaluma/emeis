import io
from tempfile import NamedTemporaryFile

import localized_fields.fields
import openpyxl
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
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

from emeis.core import utils

from . import filters, models, serializers


class BaseViewset(VisibilityViewMixin, PermissionViewMixin, views.ModelViewSet):
    def replace_prefetch(self, qs, lookup, viewset_to_use):
        """Replace prefetch with a new prefetch respecting visibilities.

        This also works if DRF didn't already add a prefetch itself.
        Pass in the lookup (name of the field to the related object)
        as well as the viewset from where the queryset should be pulled:
        When retrieving the queryset from a viewset, the visibilities
        are automatically applied.

        Return a new queryset with the prefetch replaced or added
        """

        # Hacky hacky - remove the conflicting prefetches that DRF added,
        # as otherwise the queries won't work anymore.
        # There's no "official" way to do this in the ORM, and overriding
        # DRF's get_queryset() method would be even more hacky.
        qs._prefetch_related_lookups = tuple(
            [p for p in qs._prefetch_related_lookups if lookup not in p]
        )

        # Now: prefetch using the visibility-filtered relation
        related_queryset = viewset_to_use(request=self.request).get_queryset()
        return qs.prefetch_related(Prefetch(lookup, queryset=related_queryset))


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

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "acls__role__name",
        "acls__scope__name",
        "email",
        "=zip",
        "city",
    ]

    multilingual_search_fields = [
        "city",
        "acls__role__name",
        "acls__scope__name",
    ]

    case_insensitive_ordering_fields = [
        "first_name",
        "last_name",
        "email",
        "address",
        "city",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return self.replace_prefetch(qs, "acls", ACLViewSet)

    @action(methods=["get"], detail=False)
    def export(self, request):
        """Export user list as excel table."""
        queryset = self.filter_queryset(self.get_queryset())

        # we use a template to set the headers to bold and align the columns to fit on a DIN-A4 page
        workbook = openpyxl.load_workbook(settings.USER_EXPORT_TEMPLATE_PATH)
        sheet = workbook.active

        # set column headers
        sheet["A1"] = _("Name")
        sheet["B1"] = _("First Name")
        sheet["C1"] = _("Email")
        sheet["D1"] = _("Roles and scopes")

        for row, user in enumerate(queryset.iterator(), start=2):
            acl_string = "\n".join(
                [
                    f"{acl.role.name}: {acl.scope.full_name}"
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


class MultilingualDefaultOrdering:
    """Add / modify default ordering for localized fields.

    Even though Django can deal with localized fields and will happily
    add them to "ORDER BY" clause, Postgresql's documentation states that
    this is not "particularly useful". We should sort by a specific language
    instead, even "by default".

    This adds a .order_by() call to the base queryset, using the model's
    default ordering. If the default ordering is a localized field, we
    use the currently used language for it (respecting forced-monolingual
    models as well)

    Each order_by() call will clear any previous ordering, so it's safe
    for us to "force" a default ordering here, it can still be overridden
    in regular ordering filters etc which come after
    """

    def get_queryset(self):
        qs = super().get_queryset()
        lang = utils.forced_or_current_lang(qs.model.__name__)
        ordering = qs.model._meta.ordering

        def _order_field_suffix_if_needed(field_name):
            field = qs.model._meta.get_field(field_name)
            if isinstance(field, localized_fields.fields.LocalizedField):
                return f"{field_name}__{lang}"

            return field_name

        new_ordering = [_order_field_suffix_if_needed(field) for field in ordering]

        qs = qs.order_by(*new_ordering)
        return qs


class ScopeViewSet(MultilingualDefaultOrdering, BaseViewset):
    serializer_class = serializers.ScopeSerializer
    queryset = models.Scope.objects.all()
    search_fields = (
        "name",
        "description",
    )
    multilingual_search_fields = [
        "name",
        "description",
    ]

    case_insensitive_ordering_fields = [
        "name",
        "description",
        "full_name",
    ]
    filterset_class = filters.ScopeFilterset

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.replace_prefetch(qs, "acls", ACLViewSet)

        return qs


class RoleViewSet(MultilingualDefaultOrdering, BaseViewset):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()
    search_fields = (
        "slug",
        "name",
        "description",
    )
    multilingual_search_fields = [
        "name",
        "description",
    ]

    case_insensitive_ordering_fields = [
        "name",
        "description",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return self.replace_prefetch(qs, "acls", ACLViewSet)


class PermissionViewSet(BaseViewset):
    serializer_class = serializers.PermissionSerializer
    queryset = models.Permission.objects.prefetch_related("roles")
    filterset_fields = ("roles",)
    search_fields = (
        "slug",
        "name",
        "description",
    )
    multilingual_search_fields = [
        "name",
        "description",
    ]
    case_insensitive_ordering_fields = [
        "name",
        "description",
    ]


class ACLViewSet(BaseViewset):
    serializer_class = serializers.ACLSerializer
    queryset = models.ACL.objects.all().select_related("user", "scope", "role")
    filterset_class = filters.ACLFilterset
    search_fields = [
        "scope__name",
        "scope__description",
        "role__name",
        "role__description",
        "user__username",
        "user__first_name",
        "user__last_name",
        "=user__zip",
        "user__city",
    ]

    multilingual_search_fields = [
        "scope__name",
        "scope__description",
        "role__name",
        "role__description",
        "user__city",
    ]
