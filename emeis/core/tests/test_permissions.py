import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from emeis.core.models import PermissionMixin, Scope, User
from emeis.core.permissions import (
    AllowAny,
    BasePermission,
    object_permission_for,
    permission_for,
)

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


@pytest.fixture
def reset_permission_classes():
    yield
    PermissionMixin.permission_classes = [AllowAny]


@pytest.mark.freeze_time(TIMESTAMP)
@pytest.mark.parametrize(
    "method,status",
    [
        ("post", HTTP_201_CREATED),
        ("patch", HTTP_200_OK),
        ("delete", HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_permission(
    user_factory,
    admin_user,
    admin_client,
    client,
    method,
    status,
    use_admin_client,
    reset_permission_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission(BasePermission):
        @permission_for(User)
        def has_permission_for_user(self, request):
            if request.user.username == "admin" or request.data["phone"] == "232355":
                return True
            return False

        @object_permission_for(User)
        def has_object_permission_for_user(self, request, instance):
            assert isinstance(instance, User)
            if request.user.username == "admin":
                return True
            return False

    PermissionMixin.permission_classes = [CustomPermission]

    user = user_factory(username="foo")

    url = reverse("user-list")

    data = {
        "data": {
            "type": "users",
            "attributes": {
                "meta": {},
                "username": "mark48",
                "first-name": "Amanda",
                "last-name": "Gallagher",
                "email": "banderson@example.com",
                "phone": None,
                "language": "en",
                "address": None,
                "city": None,
                "zip": None,
                "is-active": True,
            },
        }
    }

    if method in ["patch", "delete"]:
        url = reverse("user-detail", args=[user.pk])
        data["data"]["id"] = str(user.pk)

    if not use_admin_client and method == "patch":
        data["data"]["attributes"]["phone"] = "232355"

    response = getattr(client, method)(url, data=data)

    if not use_admin_client:
        assert response.status_code == HTTP_403_FORBIDDEN
        return

    assert response.status_code == status
    if method == "post":
        result = response.json()
        assert result["data"]["attributes"]["date-joined"] == TIMESTAMP
    elif method == "patch":
        user.refresh_from_db()
        assert user.username == "mark48"


def test_permission_no_permissions_configured(client, reset_permission_classes):
    PermissionMixin.permission_classes = None

    data = {
        "data": {
            "type": "users",
            "attributes": {
                "username": "mark48",
                "email": "banderson@example.com",
                "language": "en",
            },
        }
    }

    url = reverse("user-list")
    with pytest.raises(ImproperlyConfigured):
        client.post(url, data=data)


def test_custom_permission_override_has_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @permission_for(User)
        def has_permission_for_custom_mutation(self, request):  # pragma: no cover
            return False

        @permission_for(User)
        def has_permission_for_custom_mutation_2(self, request):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_object_permission_with_duplicates():
    class CustomPermission(BasePermission):
        @object_permission_for(User)
        def has_object_permission_for_custom_mutation(
            self, request, instance
        ):  # pragma: no cover
            return False

        @object_permission_for(User)
        def has_object_permission_for_custom_mutation_2(
            self, request, instance
        ):  # pragma: no cover
            return False

    with pytest.raises(ImproperlyConfigured):
        CustomPermission()


def test_custom_permission_override_has_permission_with_multiple_models(request):
    class CustomPermission(BasePermission):
        @permission_for(User)
        @permission_for(Scope)
        def has_permission_for_both_mutations(self, request):  # pragma: no cover
            return False

    assert not CustomPermission().has_permission(User, request)
    assert not CustomPermission().has_permission(Scope, request)


def test_custom_permission_override_has_object_permission_with_multiple_mutations(
    db, request, user, scope
):
    class CustomPermission(BasePermission):
        @object_permission_for(User)
        @object_permission_for(Scope)
        def has_object_permission_for_both_mutations(
            self, request, instance
        ):  # pragma: no cover
            return False

    assert not CustomPermission().has_object_permission(User, request, user)
    assert not CustomPermission().has_object_permission(Scope, request, scope)
