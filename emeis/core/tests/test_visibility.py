import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from emeis.core.models import BaseModel, Scope, User, VisibilityMixin
from emeis.core.visibilities import BaseVisibility, Union, filter_queryset_for


@pytest.mark.parametrize("detail", [True, False])
@pytest.mark.parametrize("use_admin_client", [True, False])
def test_visibility(
    user_factory,
    acl_factory,
    admin_user,
    admin_client,
    client,
    detail,
    use_admin_client,
):
    client = admin_client if use_admin_client else client

    class TestVisibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_user(self, queryset, request):
            if request.user.username != "admin":
                return queryset.none()
            return queryset.exclude(username="bar")

    VisibilityMixin.visibility_classes = [TestVisibility]

    user = user_factory(username="foo")
    user_factory(username="bar")

    url = reverse("user-list")
    if detail:
        url = reverse("user-detail", args=[user.pk])
    response = client.get(url)
    if detail and not use_admin_client:
        assert response.status_code == HTTP_404_NOT_FOUND
        return
    assert response.status_code == HTTP_200_OK
    result = response.json()
    if not detail:
        if use_admin_client:
            assert len(result["data"]) == 2
            assert sorted(
                [
                    result["data"][0]["attributes"]["username"],
                    result["data"][1]["attributes"]["username"],
                ]
            ) == ["admin", "foo"]
        else:
            assert len(result["data"]) == 0
    else:
        assert result["data"]["attributes"]["username"] == "foo"


def test_visibility_no_visibilities_configured(client):
    VisibilityMixin.visibility_classes = None

    url = reverse("user-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_visibility_dupes(client):
    class TestVisibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_user(self, queryset, request):  # pragma: no cover
            return queryset

        @filter_queryset_for(User)
        def filter_queryset_for_user2(self, queryset, request):  # pragma: no cover
            return queryset

    VisibilityMixin.visibility_classes = [TestVisibility]

    url = reverse("user-list")
    with pytest.raises(ImproperlyConfigured):
        client.get(url)


def test_custom_visibility_for_basemodel(db, client, scope_factory):
    """Test fallback to BaseModel."""
    scope_factory(name="Name1")
    scope_factory(name="Name2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

    VisibilityMixin.visibility_classes = [CustomVisibility]

    assert Scope.objects.count() == 2

    url = reverse("scope-list")
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    result = response.json()

    assert result == {"data": []}


def test_custom_visibility_override_specificity(db, user_factory):
    """The first matching filter 'wins'."""
    user_factory(username="Name1")
    user_factory(username="Name2")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(BaseModel)
        def filter_queryset_for_all(self, queryset, request):
            return queryset.none()

        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(username="Name1")

    assert User.objects.count() == 2
    queryset = CustomVisibility().filter_queryset(BaseModel, User.objects, None)
    assert queryset.count() == 0
    queryset = CustomVisibility().filter_queryset(User, User.objects, None)
    assert queryset.count() == 1


def test_union_visibility(db, user_factory):
    user_factory(username="Name1")
    user_factory(username="Name2")
    user_factory(username="Name3")
    user_factory(username="Name4")

    class Name1Visibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(username="Name1")

    class Name2Visibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(username="Name2")

    class Name3Visibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.filter(username__in=["Name2", "Name3"])

    class ConfiguredUnion(Union):
        visibility_classes = [Name1Visibility, Name2Visibility, Name3Visibility]

    queryset = User.objects
    result = Name1Visibility().filter_queryset(User, queryset, None)
    assert result.count() == 1
    result = Name2Visibility().filter_queryset(User, queryset, None)
    assert result.count() == 1
    result = Name3Visibility().filter_queryset(User, queryset, None)
    assert result.count() == 2
    queryset = ConfiguredUnion().filter_queryset(User, queryset, None)
    assert queryset.count() == 3
    assert queryset.get(username="Name2")


def test_union_visibility_none(db, user_factory):
    user_factory(username="Name1")

    class CustomVisibility(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class CustomVisibility2(BaseVisibility):
        @filter_queryset_for(User)
        def filter_queryset_for_custom_node(self, queryset, request):
            return queryset.none()

    class ConfiguredUnion(Union):
        visibility_classes = [CustomVisibility2, CustomVisibility]

    queryset = User.objects
    result = CustomVisibility().filter_queryset(User, queryset, None)
    assert result.count() == 0
    result = CustomVisibility2().filter_queryset(User, queryset, None)
    assert result.count() == 0
    queryset = ConfiguredUnion().filter_queryset(User, queryset, None)
    assert queryset.count() == 0
