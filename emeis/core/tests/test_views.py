from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
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
