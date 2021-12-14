import pytest
from django.urls import reverse
from rest_framework import status


def test_search_users(
    admin_client,
    acl_factory,
):

    users_list = [acl.user for acl in acl_factory.create_batch(5)]

    resp = admin_client.get(
        reverse("user-list"), {"filter[search]": users_list[0].first_name}
    )

    returned_user_ids = [us["id"] for us in resp.json()["data"]]

    assert str(users_list[0].pk) in returned_user_ids


@pytest.mark.parametrize(
    "filter_name, expect_result",
    [("hasRole", True), ("has_role", True), ("hasrole", False)],
)
def test_user_has_role(admin_client, acl_factory, filter_name, expect_result):
    users_list = [acl.user for acl in acl_factory.create_batch(3)]

    resp = admin_client.get(
        reverse("user-list"),
        {f"filter[{filter_name}]": users_list[2].acls.first().role_id},
    )

    if expect_result:
        ret_users = [us["attributes"]["username"] for us in resp.json()["data"]]
        expected = [str(users_list[2].username)]

        assert expected == ret_users
    else:
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "filter_field, model_attr, expect_result",
    [
        ("id__in", "pk", True),
        ("id", "pk", True),
        ("username", "username", True),
        ("username", "email", False),
        ("email__in", "email", True),
        ("email__in", "username", False),
    ],
)
def test_declared_filters(
    admin_client, user_factory, filter_field, model_attr, expect_result
):
    user1, _ = user_factory.create_batch(2)

    attr_value = getattr(user1, model_attr)

    resp = admin_client.get(
        reverse("user-list"), {f"filter[{filter_field}]": attr_value}
    )

    ret_users = [us["attributes"]["username"] for us in resp.json()["data"]]

    if expect_result:
        assert [user1.username] == ret_users
    else:
        assert ret_users == []
