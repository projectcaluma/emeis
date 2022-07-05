import pytest
from django.urls import reverse
from django.utils import translation
from rest_framework import status

from emeis.core.models import User


@pytest.mark.parametrize(
    "user_attribute",
    [
        lambda u: u.first_name,
        lambda u: u.last_name,
        lambda u: u.acls.first().scope.name,
        lambda u: u.acls.first().role.name,
    ],
)
@pytest.mark.parametrize(
    "partial_search", [lambda val: val[:-2], lambda val: val[2:], lambda val: val]
)
def test_search_users(admin_client, acl_factory, user_attribute, partial_search):

    users_list = [acl.user for acl in acl_factory.create_batch(5)]

    resp = admin_client.get(
        reverse("user-list"),
        {"filter[search]": partial_search(str(user_attribute(users_list[0])))},
    )
    returned_user_ids = [us["id"] for us in resp.json()["data"]]

    assert str(users_list[0].pk) in returned_user_ids
    # ensure we don't just return the full user list
    assert len(returned_user_ids) < len(users_list)


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
    "filter_value, expect_count",
    [("true", 4), ("false", 2)],
)
def test_user_is_active_filter(admin_client, user_factory, filter_value, expect_count):
    user_factory.create_batch(3, is_active=True)
    user_factory.create_batch(2, is_active=False)

    resp = admin_client.get(
        reverse("user-list"),
        {"filter[is_active]": filter_value},
    )

    assert len(resp.json()["data"]) == expect_count


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


@pytest.mark.parametrize(
    "filter_field, model_attr",
    [
        ("user__in", "user_id"),
        ("role__in", "role_id"),
        ("scope__in", "scope_id"),
    ],
)
def test_acl_filters(admin_client, acl_factory, filter_field, model_attr):
    acl1, acl2, _ = acl_factory.create_batch(3)

    attr_value_1 = getattr(acl1, model_attr)
    attr_value_2 = getattr(acl2, model_attr)

    resp = admin_client.get(
        reverse("acl-list"),
        {f"filter[{filter_field}]": f"{attr_value_1},{attr_value_2}"},
    )

    ret_acls = [acl["id"] for acl in resp.json()["data"]]
    assert set([str(acl1.pk), str(acl2.pk)]) == set(ret_acls)


def test_scope_id_filter(admin_client, scope_factory):
    scope1, _, scope3 = scope_factory.create_batch(3)

    resp = admin_client.get(
        reverse("scope-list"),
        {"filter[id__in]": ",".join([str(scope1.pk), str(scope3.pk)])},
    )

    ret_scopes = [us["id"] for us in resp.json()["data"]]

    assert set(ret_scopes) == set([str(scope1.pk), str(scope3.pk)])


@pytest.mark.parametrize("sort", ["email", "-email"])
def test_user_ordering_case_insensitive(admin_client, admin_user, user_factory, sort):
    emails = [
        "Aaaa@example.com",
        "Zzzzz@example.com",
        "aaaaa@example.com",
        "m@example.com",
    ]
    for email in emails:
        user_factory.create(email=email)

    resp = admin_client.get(reverse("user-list"), {"sort": sort})

    expect_emails = sorted(
        emails + [admin_user.user.email],
        key=lambda e: e.lower(),
        reverse=sort.startswith("-"),
    )

    assert expect_emails == [d["attributes"]["email"] for d in resp.json()["data"]]


@pytest.mark.parametrize("sort", ["metainfo__position", "-metainfo__position"])
def test_ordering_metainfo(admin_client, admin_user, user_factory, sort, settings):
    settings.EMEIS_META_FIELDS = ["position"]
    admin_user.user.metainfo = {"position": "d"}
    admin_user.user.save()
    positions = ["B", "a", "C"]
    for position in positions:
        user_factory.create(metainfo={"position": position})

    resp = admin_client.get(reverse("user-list"), {"sort": sort})

    expect = sorted(
        positions + ["d"], key=lambda e: e.lower(), reverse=sort.startswith("-")
    )

    assert expect == [
        d["attributes"]["metainfo"].get("position") for d in resp.json()["data"]
    ]


@pytest.mark.parametrize("sort", ["username", "-username"])
def test_user_ordering_case_sensitive(admin_client, admin_user, user_factory, sort):
    user_factory.create_batch(5)

    resp = admin_client.get(reverse("user-list"), {"sort": sort})

    expected = list(
        User.objects.all().order_by(sort).values_list("username", flat=True)
    )

    assert expected == [d["attributes"]["username"] for d in resp.json()["data"]]


@pytest.mark.parametrize(
    "force_lang, search_term, expect_result",
    [
        ("de", "deutscher", 1),
        ("de", "english", 0),
        ("en", "deutscher", 0),
        ("en", "english", 1),
        (None, "deutscher", 0),
        (None, "english", 1),
    ],
)
def test_search_monolingual(
    settings, admin_client, role_factory, force_lang, search_term, expect_result
):
    role_factory(name={"de": "deutscher name", "en": "english name"})

    if force_lang:
        settings.EMEIS_FORCE_MODEL_LOCALE = {"role": force_lang}

    with translation.override("en"):
        resp = admin_client.get(reverse("role-list"), {"filter[search]": search_term})

    assert len(resp.json()["data"]) == expect_result


@pytest.mark.parametrize(
    "search_term, expect_result",
    [
        ("foobar", 1),
        ("bar", 2),
        ("buzzybuzz", 0),
    ],
)
def test_search_metainfo(
    settings, admin_client, user_factory, search_term, expect_result
):
    settings.EMEIS_META_FIELDS = ["position"]
    user_factory(metainfo={"position": "bar"})
    user_factory(metainfo={"position": "baz"})
    user_factory(metainfo={"blubb": "bar"})
    user_factory(metainfo={"position": "Foobar"})

    resp = admin_client.get(reverse("user-list"), {"filter[search]": search_term})

    assert len(resp.json()["data"]) == expect_result
