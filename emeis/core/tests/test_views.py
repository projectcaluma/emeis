import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED


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
