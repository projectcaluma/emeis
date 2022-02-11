from uuid import uuid4

import pyexcel
import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)


def test_me_200(db, acl, client):
    client.force_authenticate(user=acl.user)
    url = reverse("me-detail")

    response = client.get(url, data={"include": "acls"})

    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["included"]) == 1
    assert (
        result["data"]["id"]
        == result["included"][0]["relationships"]["user"]["data"]["id"]
        == str(acl.user.pk)
    )
    assert result["included"][0]["id"] == str(acl.pk)


@pytest.mark.parametrize(
    "method,status_code",
    [
        ("post", HTTP_405_METHOD_NOT_ALLOWED),
        ("patch", HTTP_405_METHOD_NOT_ALLOWED),
        ("put", HTTP_405_METHOD_NOT_ALLOWED),
        ("head", HTTP_200_OK),
        ("options", HTTP_200_OK),
    ],
)
def test_me_405(db, acl, client, method, status_code):
    client.force_authenticate(user=acl.user)
    url = reverse("me-detail")

    response = getattr(client, method)(url)

    assert response.status_code == status_code


@pytest.mark.parametrize("list", [True, False])
def test_myacls_200(db, acl_factory, client, list):
    acl = acl_factory(role__slug="my-role")
    acl_factory()
    client.force_authenticate(user=acl.user)
    url = reverse("myacls-list")
    if not list:
        url = reverse("myacls-detail", args=[acl.pk])

    response = client.get(url, data={"include": "role"})

    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["included"]) == 1
    if list:
        assert result["data"][0]["id"] == str(acl.pk)
        assert len(result["data"]) == 1
    else:
        assert result["data"]["id"] == str(acl.pk)


def test_myacls_404(db, user, client):
    client.force_authenticate(user=user)
    url = reverse("myacls-detail", args=[str(uuid4())])

    response = client.get(url)

    assert response.status_code == HTTP_404_NOT_FOUND


def test_myacls_403(db, acl_factory, user, client):
    acl = acl_factory()
    client.force_authenticate(user=user)
    url = reverse("myacls-detail", args=[str(acl.pk)])

    response = client.get(url)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_search_filter(db, user_factory, client):
    user_factory(username="user1", city="Lucerne", zip="6000", last_name="Kafka")
    user_factory(username="user2", city="Berne", zip="5000", last_name="Smith")
    user_factory(username="user3", city="Zurich", zip="8000", last_name="Smith")

    url = reverse("user-list")

    response = client.get(url, {"filter[search]": "bern"})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 1
    assert result["data"][0]["attributes"]["username"] == "user2"

    response = client.get(url, {"filter[search]": "8000"})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 1
    assert result["data"][0]["attributes"]["username"] == "user3"

    response = client.get(url, {"filter[search]": "smith"})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 2
    assert "user1" not in (
        result["data"][0]["attributes"]["username"],
        result["data"][1]["attributes"]["username"],
    )


def test_scope_search_filter(db, scope_factory, client):
    scope_factory(name="scope1")
    scope_factory(name={"de": "skop2", "en": "scope2"})
    scope_factory(name="scope3")

    url = reverse("scope-list")

    response = client.get(url, {"filter[search]": "skop"}, HTTP_ACCEPT_LANGUAGE="de")

    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 1
    assert result["data"][0]["attributes"]["name"] == {
        "de": "skop2",
        "en": "scope2",
        "fr": "",
    }
    assert result["data"][0]["attributes"]["level"] == 0

    response = client.get(url, {"filter[search]": "scope"})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 3


def test_scope_full_name_api(db, scope_factory, client):
    parent = scope_factory()
    child = scope_factory(parent=parent)

    url = reverse("scope-detail", args=[child.pk])
    response = client.get(url)

    full_name = response.json()["data"]["attributes"]["full-name"]
    assert full_name["en"] == child.full_name(language="en")
    assert full_name["en"].startswith(parent.name["en"])
    assert full_name["en"].endswith(child.name["en"])


def test_cannot_write_level(db, client, settings, user):
    data = {
        "data": {
            "type": "scopes",
            "attributes": {"name": {"en": "test"}, "level": 400},
        }
    }

    resp = client.post(reverse("scope-list"), data=data)

    assert resp.status_code == HTTP_201_CREATED
    result = resp.json()
    assert result["data"]["attributes"]["level"] == 0


def test_acl_user_filter(db, user, acl_factory, client):
    acl = acl_factory(user=user)
    acl_factory()

    url = reverse("acl-list")

    response = client.get(url, {"filter[user]": acl.user.pk})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == str(acl.pk)
    assert result["data"][0]["relationships"]["user"]["data"]["id"] == str(acl.user.pk)


def test_acl_search_filter(db, acl_factory, client):
    acl = acl_factory(role__name="scope1", scope__name="scope1", user__username="user1")
    acl_factory(role__name="scope1", scope__name="scope2", user=acl.user)
    acl_factory(role__name="scope1", scope=acl.scope, user__username="user2")

    url = reverse("acl-list")

    response = client.get(url, {"filter[search]": "user1"})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 2
    assert (
        result["data"][0]["relationships"]["user"]["data"]["id"]
        == result["data"][1]["relationships"]["user"]["data"]["id"]
        == str(acl.user.pk)
    )


def test_permission_role_filter(db, user, role_factory, permission_factory, client):
    permission = permission_factory()
    role = role_factory()
    role.permissions.add(permission)

    dummy_permission = permission_factory()
    dummy_role = role_factory()
    dummy_role.permissions.add(dummy_permission)

    url = reverse("permission-list")

    response = client.get(url, {"filter[roles]": role.pk})
    assert response.status_code == HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == 1
    assert result["data"][0]["id"] == str(permission.pk)


@pytest.mark.parametrize("allow_anon", [True, False])
@pytest.mark.parametrize("method", ["post", "patch"])
def test_anonymous_writing(db, client, settings, user, allow_anon, method):
    settings.ALLOW_ANONYMOUS_WRITE = allow_anon
    if not allow_anon:
        settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
            "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        ]

    data = {
        "data": {
            "type": "users",
            "attributes": {"username": "winstonsmith", "language": "en"},
        }
    }

    url = reverse("user-list")

    if method == "patch":
        data["data"]["id"] = str(user.pk)
        url = reverse("user-detail", args=[user.pk])

    resp = getattr(client, method)(url, data=data)
    assert (
        resp.status_code == HTTP_201_CREATED or HTTP_200_OK
        if allow_anon
        else HTTP_403_FORBIDDEN
    )


def test_user_export(client, user_factory, acl_factory, snapshot):
    user = user_factory()
    acl_factory.create_batch(9)
    acl_factory.create_batch(2, user=user)

    url = reverse("user-export")

    response = client.get(url)

    assert response.status_code == HTTP_200_OK

    book = pyexcel.get_book(file_content=response.getvalue(), file_type="xlsx")
    sheet = book.bookdict.popitem()[1]

    snapshot.assert_match(sheet)
