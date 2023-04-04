from unicodedata import normalize

import pytest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import BaseUserManager
from django.utils import translation
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


def test_scope_deletion(db, scope_factory):
    root = scope_factory()  # not deleted
    child = scope_factory(parent=root)
    grandchild = scope_factory(parent=child)
    scope_factory(parent=grandchild)
    scope_factory(parent=grandchild)

    other_child = scope_factory(parent=root)  # not deleted
    scope_factory(parent=other_child)  # not deleted

    child.delete()

    assert Scope.objects.count() == 3
    assert list(Scope.objects.root_nodes()) == [root]


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
        grandchild.full_name
        == f"{root.name} \u00bb {child.name} \u00bb {grandchild.name}"
    )


@pytest.mark.parametrize(
    "language, expected",
    [
        ("de", "DE ROOT » FR CHILD » DE GRANDCHILD"),
        ("fr", "DE ROOT » FR CHILD » FR GRANDCHILD"),
    ],
)
def test_scope_hierarchical_name_fallbacks(
    db, language, scope_factory, expected, settings
):
    settings.LANGUAGE_CODE = "de"
    settings.LANGUAGES = [("de", "de"), ("fr", "fr")]
    settings.LOCALIZED_FIELDS_FALLBACKS = {"fr": ["de"], "de": ["fr"]}
    with translation.override(language):
        root = scope_factory()
        root.name = {"de": "DE ROOT"}
        root.save()
        child = scope_factory(parent=root)
        child.name = {"fr": "FR CHILD"}
        child.save()
        grandchild = scope_factory(parent=child)
        grandchild.name = {"de": "DE GRANDCHILD", "fr": "FR GRANDCHILD"}
        grandchild.save()

        assert str(grandchild.full_name) == expected


@pytest.mark.parametrize("language", ["de", "fr"])
def test_scope_fullname_when_forced_language(db, language, scope_factory, settings):
    settings.LANGUAGE_CODE = "de"
    settings.LANGUAGES = [("de", "de"), ("fr", "fr")]
    settings.EMEIS_FORCE_MODEL_LOCALE = {"scope": "de"}

    with translation.override(language):
        root = scope_factory(name="DE ROOT")
        child = scope_factory(parent=root, name={"de": "DE CHILD", "fr": "FR CHILD"})
        grandchild = scope_factory(
            parent=child, name={"de": "DE GRANDCHILD", "fr": "FR GRANDCHILD"}
        )

        # Trigger pre_save `set_full_name()` hook
        grandchild.save()
        assert grandchild.full_name.de == "DE ROOT » DE CHILD » DE GRANDCHILD"
        assert grandchild.full_name.fr == ""


def test_update_full_name_of_child(db, scope_factory):
    root = scope_factory(parent=None, name="r")
    child = scope_factory(parent=root, name="c")
    grandchild = scope_factory(parent=child, name="g")

    # full name should be r -> c -> g
    assert str(grandchild.full_name) == "r » c » g"

    sibling = scope_factory(parent=root, name="s")

    # move parent of grandchild - this should trigger an
    # update on the grandchild's full name
    child.parent = sibling
    child.save()

    grandchild.refresh_from_db()
    assert str(grandchild.full_name) == "r » s » c » g"
