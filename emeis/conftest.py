import importlib
import inspect

import pytest
from django.core.cache import cache
from django.utils.module_loading import import_string
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

from emeis.core.models import ACL, Role, Scope, User


def register_module(module):
    for _, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            # name needs to be compatible with
            # `rest_framework.routers.SimpleRouter` naming for easier testing
            base_name = obj._meta.model._meta.object_name.lower()
            register(obj, base_name)


register_module(importlib.import_module(".core.factories", "emeis"))


@pytest.fixture
def admin_user(db, user, settings):
    user.username = "admin"
    user.save()

    user_factory = import_string(settings.EMEIS_OIDC_USER_FACTORY)
    return user_factory("admin", {settings.OIDC_USERNAME_CLAIM: "admin"})


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def client(db):
    client = APIClient()
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture(autouse=True)
def _remove_bootstrap_data(db):
    for model in [User, Scope, Role, ACL]:
        getattr(model, "objects").all().delete()
