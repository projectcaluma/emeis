from datetime import datetime

from django.utils import timezone
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class UserFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("user_name")
    email = Faker("safe_email")
    last_login = datetime(
        2021, 7, 20, 12, 00, 00, tzinfo=timezone.get_default_timezone()
    )
    password = Faker("password")
    language = "en"

    class Meta:
        model = models.User


class ScopeFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("text")
    parent = None

    class Meta:
        model = models.Scope


class RoleFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Role


class PermissionFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("name")
    description = Faker("text")

    class Meta:
        model = models.Permission


class RolePermissionFactory(DjangoModelFactory):
    role = SubFactory(RoleFactory)
    permission = SubFactory(PermissionFactory)

    class Meta:
        model = models.Role.permissions.through


class ACLFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    scope = SubFactory(ScopeFactory)
    role = SubFactory(RoleFactory)

    class Meta:
        model = models.ACL
