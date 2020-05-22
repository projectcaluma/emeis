from unicodedata import normalize

from django.contrib.auth.base_user import BaseUserManager
from django.urls import reverse
from hypothesis import given
from hypothesis.strategies import emails, text
from rest_framework import status

from ..models import User


def test_user_model():
    user = User(
        username="foobar", email="foo@example.com", first_name="Foo", last_name="Bar"
    )
    assert user.get_full_name() == "Foo Bar"
    assert user.natural_key() == user.username
    assert user.get_email_field_name() == "email"
    assert user.is_anonymous is False
    assert user.is_authenticated is True


@given(username=text(), email=emails())
def test_user_model_normalization(username, email):
    username_normal = normalize("NFKC", username)
    email_normal = BaseUserManager.normalize_email(email)
    user = User(username=username, email=email, first_name="Foo", last_name="Bar")
    user.clean()
    assert user.username == username_normal
    assert user.email == email_normal


def test_user_detail(admin_user, admin_client):
    url = reverse("user-detail", args=[admin_user.id])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["data"]["id"] == str(admin_user.id)
    assert "password" not in json["data"]["attributes"]
