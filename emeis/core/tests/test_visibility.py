import pytest
from django.apps import apps
from django.urls import reverse

from emeis.oidc_auth.authentication import OIDCUser


@pytest.mark.parametrize("requesting_user", ["anon", "user", "admin"])
def test_own_and_admin_visibility(
    db,
    user_factory,
    scope_factory,
    role_factory,
    permission_factory,
    acl_factory,
    admin_user,
    settings,
    client,
    requesting_user,
):

    settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES = [
        "emeis.core.visibilities.OwnAndAdmin"
    ]
    apps.get_app_config("generic_permissions").ready()

    user = user_factory()

    expected_count = 0
    if requesting_user == "admin":
        client.force_authenticate(
            OIDCUser(username=admin_user.username, claims={"sub": admin_user.username})
        )
        expected_count = 2
    elif requesting_user == "user":
        client.force_authenticate(
            OIDCUser(username=user.username, claims={"sub": user.username})
        )
        expected_count = 1

    scope1 = scope_factory()
    scope2 = scope_factory()

    role1 = role_factory()
    role2 = role_factory()

    perm1 = permission_factory()
    permission_factory()

    role1.permissions.add(perm1)

    acl_factory(user=user, scope=scope1, role=role1)
    acl_factory(user=admin_user.user, scope=scope2, role=role2)

    resp = client.get(reverse("user-list"))
    assert len(resp.json()["data"]) == expected_count

    resp = client.get(reverse("scope-list"))
    assert len(resp.json()["data"]) == expected_count

    resp = client.get(reverse("role-list"))
    assert len(resp.json()["data"]) == expected_count

    resp = client.get(reverse("permission-list"))
    assert len(resp.json()["data"]) == expected_count

    resp = client.get(reverse("acl-list"))
    assert len(resp.json()["data"]) == (2 if requesting_user == "admin" else 0)
