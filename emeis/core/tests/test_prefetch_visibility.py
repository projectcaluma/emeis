import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from emeis.core import models
from emeis.core.visibilities import filter_queryset_for


class TestACLVisibility:
    @filter_queryset_for(models.ACL)
    def filter_queryset_for_acl(self, queryset, request):
        return queryset.filter(role__slug="foo")


@pytest.mark.parametrize("include", ["acls", ""])
@pytest.mark.freeze_time("2017-05-21")
def test_invisible_acl_in_users(
    admin_client,
    set_visibilities,
    user_factory,
    role_factory,
    acl_factory,
    include,
):
    role_foo = role_factory(slug="foo")
    role_bar = role_factory(slug="bar")
    url = reverse("user-list")

    user1, user2 = user_factory.create_batch(2)
    # both users have both roles in an ACL. However only the "foo"
    # ACL should be returned in the includes and relationships
    acl_factory(role=role_foo, user=user1)
    acl_factory(role=role_foo, user=user2)
    acl_factory(role=role_bar, user=user1)
    acl_factory(role=role_bar, user=user2)

    set_visibilities(["emeis.core.tests.test_prefetch_visibility.TestACLVisibility"])

    with CaptureQueriesContext(connection) as context:
        resp = admin_client.get(url, {"include": include})

    assert len(context.captured_queries) == 2

    collected_acl_rels = [
        acl["id"]
        for u in resp.json()["data"]
        for acl in u["relationships"]["acls"]["data"]
    ]
    related_roles = models.Role.objects.filter(acls__in=collected_acl_rels)
    assert role_bar not in related_roles

    if include:
        collected_acl_includes = [
            inc["id"] for inc in resp.json()["included"] if inc["type"] == "acls"
        ]
        included_roles = models.Role.objects.filter(acls__in=collected_acl_includes)
        assert role_bar not in included_roles


@pytest.mark.parametrize("include", ["acls", "acls.role", "acls.role,acls.scope"])
@pytest.mark.freeze_time("2017-05-21")
def test_number_of_queries(
    admin_client,
    set_visibilities,
    user_factory,
    role_factory,
    acl_factory,
    include,
):
    role_foo = role_factory(slug="foo")
    role_bar = role_factory(slug="bar")
    url = reverse("user-list")

    def create_some():
        user1, user2 = user_factory.create_batch(2)
        # both users have both roles in an ACL. However only the "foo"
        # ACL should be returned in the includes and relationships
        acl_factory(role=role_foo, user=user1)
        acl_factory(role=role_foo, user=user2)
        acl_factory(role=role_bar, user=user1)
        acl_factory(role=role_bar, user=user2)
        return user1, user2

    set_visibilities(["emeis.core.tests.test_prefetch_visibility.TestACLVisibility"])

    create_some()

    with CaptureQueriesContext(connection) as context:
        admin_client.get(url, {"include": include})
    num_queries = len(context.captured_queries)

    create_some()

    with CaptureQueriesContext(connection) as context:
        admin_client.get(url, {"include": include})

    # We need to be sure that we don't create N+1 problems: Regardless of
    # includes, and regardless of number of users, the number of queries
    # must not change
    assert num_queries == len(context.captured_queries)
