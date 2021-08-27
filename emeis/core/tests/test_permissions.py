import pytest
from django.urls import reverse
from generic_permissions.config import ObjectPermissionsConfig, PermissionsConfig
from generic_permissions.permissions import object_permission_for, permission_for
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)

from emeis.core.models import User

TIMESTAMP = "2017-05-21T11:25:41.123840Z"


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
    reset_config_classes,
):
    client = admin_client if use_admin_client else client

    class CustomPermission:
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

    PermissionsConfig.register_handler_class(CustomPermission)
    ObjectPermissionsConfig.register_handler_class(CustomPermission)

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
