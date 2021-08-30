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
    user,
    requesting_user,
):

    settings.GENERIC_PERMISSIONS_VISIBILITY_CLASSES = [
        "emeis.core.visibilities.OwnAndAdmin"
    ]
    apps.get_app_config("generic_permissions").ready()

    admin_role = role_factory(slug="admin")

    other_user = user_factory()

    scope1 = scope_factory()
    role1 = role_factory()
    perm1 = permission_factory()
    permission_factory()
    role1.permissions.add(perm1)
    acl_factory(user=user, scope=scope1, role=role1)

    expected_count = 0
    if requesting_user == "admin":
        client.force_authenticate(
            OIDCUser(username=admin_user.username, claims={"sub": admin_user.username})
        )
        user.acls.create(role=admin_role, scope=scope_factory())
        expected_count = 2
    elif requesting_user == "user":
        client.force_authenticate(
            OIDCUser(username=other_user.username, claims={"sub": other_user.username})
        )
        acl_factory(user=other_user, role=role1)
        expected_count = 1

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
