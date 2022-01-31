from unicodedata import normalize

import pytest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import BaseUserManager
from hypothesis import given
from hypothesis.strategies import emails, text
from mptt.exceptions import InvalidMove

from ..models import Scope, User


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


def test_scope_model(db):
    parent_scope = Scope.objects.create(name="parent scope")
    scope = Scope.objects.create(name="child scope", parent=parent_scope)

    assert scope.parent.name["en"] == "parent scope"

    parent_scope.parent = scope
    with pytest.raises(InvalidMove):
        parent_scope.save()


def test_can_authenticate(db, user):
    # Test whether the authentication mechanism works correctly
    user.set_password("test_password")
    user.save()

    backend = ModelBackend()

    request = None
    auth = backend.authenticate(
        request, username=user.username, password="test_password"
    )
    assert auth == user


def test_scope_hierarchical_name(db, scope_factory):
    root = scope_factory()
    child = scope_factory(parent=root)
    grandchild = scope_factory(parent=child)

    assert (
        grandchild.full_name(sep=">")
        == f"{root.name} > {child.name} > {grandchild.name}"
    )
