from unicodedata import normalize

import pytest
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import translation
from hypothesis import given
from hypothesis.strategies import emails, text

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
    with pytest.raises(ValidationError) as excinfo:
        parent_scope.save()
    assert excinfo.match("A node cannot be made a descendant or parent of itself")


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

    assert list(Scope.objects.filter(parent=None)) == [root]


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

        # Trigger pre_save `set_full_name_and_parents()` hook
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


@pytest.fixture
def simple_tree_structure(db, scope_factory):
    # root1
    #    - sub1sub1
    #        - sub1sub1sub1
    #        - sub1sub1sub2
    #    - sub1sub2
    # root2
    #    - sub2sub1
    #    - sub2sub2
    root1 = scope_factory(name="root1")
    root2 = scope_factory(name="root2")
    sub1sub1 = scope_factory(parent=root1, name="sub1sub1")
    sub1sub2 = scope_factory(parent=root1, name="sub1sub2")
    sub1sub1sub1 = scope_factory(parent=sub1sub1, name="sub1sub1sub1")
    sub1sub1sub2 = scope_factory(parent=sub1sub1, name="sub1sub1sub2")

    sub2sub1 = scope_factory(parent=root2, name="sub2sub1")
    sub2sub2 = scope_factory(parent=root2, name="sub2sub2")
    return {
        "root1": root1,
        "root2": root2,
        "sub1sub1": sub1sub1,
        "sub1sub2": sub1sub2,
        "sub1sub1sub1": sub1sub1sub1,
        "sub1sub1sub2": sub1sub1sub2,
        "sub2sub1": sub2sub1,
        "sub2sub2": sub2sub2,
    }


@pytest.mark.parametrize(
    "include_self, expect_count",
    [
        (True, 5),
        (False, 3),
    ],
)
def test_scope_qs_ancestors(db, simple_tree_structure, include_self, expect_count):
    qs = Scope.objects.filter(
        pk__in=[
            simple_tree_structure["sub2sub2"].pk,
            simple_tree_structure["sub1sub1sub2"].pk,
        ]
    )

    ancestors_qs = qs.all_ancestors(include_self=include_self)
    # the direct and indirect ancestors must be there
    assert simple_tree_structure["root2"] in ancestors_qs
    assert simple_tree_structure["root1"] in ancestors_qs
    assert simple_tree_structure["sub1sub1"] in ancestors_qs

    if include_self:
        assert simple_tree_structure["sub2sub2"] in ancestors_qs
        assert simple_tree_structure["sub1sub1sub2"] in ancestors_qs
    else:
        assert simple_tree_structure["sub2sub2"] not in ancestors_qs
        assert simple_tree_structure["sub1sub1sub2"] not in ancestors_qs

    # ... and nothing else
    assert ancestors_qs.count() == expect_count


@pytest.mark.parametrize(
    "include_self, expect_count",
    [
        (True, 6),
        (False, 4),
    ],
)
def test_scope_qs_descendants(db, simple_tree_structure, include_self, expect_count):
    qs = Scope.objects.filter(
        pk__in=[simple_tree_structure["sub1sub1"].pk, simple_tree_structure["root2"].pk]
    )

    descendants_qs = qs.all_descendants(include_self=include_self)
    # the direct and indirect descendants must be there
    assert simple_tree_structure["sub1sub1sub1"] in descendants_qs
    assert simple_tree_structure["sub1sub1sub2"] in descendants_qs
    assert simple_tree_structure["sub2sub1"] in descendants_qs
    assert simple_tree_structure["sub2sub2"] in descendants_qs

    if include_self:
        assert simple_tree_structure["sub1sub1"] in descendants_qs
        assert simple_tree_structure["root2"] in descendants_qs
    else:
        assert simple_tree_structure["sub1sub1"] not in descendants_qs
        assert simple_tree_structure["root2"] not in descendants_qs

    # ... and nothing else
    assert descendants_qs.count() == expect_count


def test_get_root(db, simple_tree_structure):
    assert (
        simple_tree_structure["sub1sub2"].get_root() == simple_tree_structure["root1"]
    )
    assert (
        simple_tree_structure["sub1sub1"].get_root() == simple_tree_structure["root1"]
    )
    assert (
        simple_tree_structure["sub2sub2"].get_root() == simple_tree_structure["root2"]
    )
    assert (
        simple_tree_structure["sub2sub1"].get_root() == simple_tree_structure["root2"]
    )
    assert (
        simple_tree_structure["sub1sub1sub2"].get_root()
        == simple_tree_structure["root1"]
    )

    assert simple_tree_structure["root1"].get_root() == simple_tree_structure["root1"]


def test_all_roots(db, simple_tree_structure):
    qs1 = Scope.objects.filter(
        pk__in=[
            simple_tree_structure["sub1sub1sub1"].pk,
            simple_tree_structure["sub1sub2"].pk,
        ]
    ).all_roots()
    assert qs1.count() == 1
    assert qs1.filter(pk=simple_tree_structure["root1"].pk).exists()

    qs2 = Scope.objects.filter(
        pk__in=[
            simple_tree_structure["sub1sub1sub1"].pk,
            simple_tree_structure["sub2sub2"].pk,
        ]
    ).all_roots()
    assert qs2.count() == 2
    assert qs2.filter(pk=simple_tree_structure["root1"].pk).exists()
    assert qs2.filter(pk=simple_tree_structure["root2"].pk).exists()


def test_scope_factory_all_parents(simple_tree_structure):
    # This tests more the factory than anything else, but it's important we
    # validate our assumptions to guarantee the other tests do the right thing
    root1 = simple_tree_structure["root1"]
    root2 = simple_tree_structure["root2"]
    sub1sub1 = simple_tree_structure["sub1sub1"]
    sub1sub2 = simple_tree_structure["sub1sub2"]
    sub1sub1sub1 = simple_tree_structure["sub1sub1sub1"]
    sub1sub1sub2 = simple_tree_structure["sub1sub1sub2"]
    sub2sub1 = simple_tree_structure["sub2sub1"]
    sub2sub2 = simple_tree_structure["sub2sub2"]

    assert root1.all_parents == []
    assert root2.all_parents == []
    assert sub1sub1.all_parents == [root1.pk]
    assert sub1sub2.all_parents == [root1.pk]
    assert sub1sub1sub1.all_parents == [root1.pk, sub1sub1.pk]
    assert sub1sub1sub2.all_parents == [root1.pk, sub1sub1.pk]
    assert sub2sub1.all_parents == [root2.pk]
    assert sub2sub2.all_parents == [root2.pk]


def test_scope_ancestors(simple_tree_structure):
    root1 = simple_tree_structure["root1"]
    sub1sub1 = simple_tree_structure["sub1sub1"]
    sub1sub1sub1 = simple_tree_structure["sub1sub1sub1"]

    assert root1.ancestors().count() == 0
    assert list(root1.ancestors(include_self=True)) == [root1]
    assert root1 in root1.ancestors(include_self=True)

    assert list(sub1sub1sub1.ancestors()) == [root1, sub1sub1]
    assert set(sub1sub1sub1.ancestors(include_self=True)) == set(
        [
            sub1sub1,
            sub1sub1sub1,
            root1,
        ]
    )


def test_scope_descendants(simple_tree_structure):
    root1 = simple_tree_structure["root1"]
    sub1sub1 = simple_tree_structure["sub1sub1"]
    sub1sub2 = simple_tree_structure["sub1sub2"]
    sub1sub1sub1 = simple_tree_structure["sub1sub1sub1"]
    sub1sub1sub2 = simple_tree_structure["sub1sub1sub2"]

    assert set(root1.descendants()) == set(
        [
            sub1sub1,
            sub1sub2,
            sub1sub1sub1,
            sub1sub1sub2,
        ]
    )

    assert set(root1.descendants(include_self=True)) == set(
        [
            root1,
            sub1sub1,
            sub1sub2,
            sub1sub1sub1,
            sub1sub1sub2,
        ]
    )
