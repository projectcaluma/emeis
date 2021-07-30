import inspect

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

from . import models
from .collections import list_duplicates


def filter_queryset_for(model):
    """Decorate function to define filtering of queryset of specific model."""

    def decorate(fn):
        if not hasattr(fn, "_visibilities"):
            fn._visibilities = []

        fn._visibilities.append(model)
        return fn

    return decorate


class BaseVisibility(object):
    """Basic visibility classes to be extended by any visibility implementation.

    In combination with the decorator `@filter_queryset_for` a custom visibility class
    can define filtering on basis of models.

    A custom visibility class could look like this:
    ```
    >>> from emeis.core.visibilities import BaseVisibility
    ... from emeis.core.models import BaseModel, Scope
    ...
    ...
    ... class CustomVisibility(BaseVisibility):
    ...     @filter_queryset_for(BaseModel)
    ...     def filter_queryset_for_all(self, queryset, request):
    ...         return queryset.filter(created_by_user=request.user.username)
    ...
    ...     @filter_queryset_for(Scope)
    ...     def filter_queryset_for_scope(self, queryset, request):
    ...         return queryset.exclude(slug='protected-scope')
    """

    def __init__(self):
        queryset_fns = inspect.getmembers(self, lambda m: hasattr(m, "_visibilities"))
        queryset_nodes = [
            node.__name__ for _, fn in queryset_fns for node in fn._visibilities
        ]
        queryset_nodes_dups = list_duplicates(queryset_nodes)
        if queryset_nodes_dups:
            raise ImproperlyConfigured(
                f"`filter_queryset_for` defined multiple times for "
                f"{', '.join(queryset_nodes_dups)} in {str(self)}"
            )
        self._filter_querysets_for = {
            node: fn for _, fn in queryset_fns for node in fn._visibilities
        }

    def filter_queryset(self, model, queryset, request):
        for cls in model.mro():
            if cls in self._filter_querysets_for:
                return self._filter_querysets_for[cls](queryset, request)

        return queryset


class Any(BaseVisibility):
    """No restrictions, all models are exposed."""

    pass


class OwnAndAdmin(BaseVisibility):
    @staticmethod
    def generic_own_and_admin(request, queryset, _filters_cb=lambda: {}, none=False):
        if isinstance(request.user, AnonymousUser):
            return queryset.none()
        elif request.user.username == settings.ADMIN_USERNAME:
            return queryset
        if none:
            return queryset.none()
        return queryset.filter(**_filters_cb())

    @filter_queryset_for(models.User)
    def filter_queryset_for_user(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"pk": request.user.user.pk}
        )

    @filter_queryset_for(models.Scope)
    @filter_queryset_for(models.Role)
    def filter_queryset_for_scope_and_role(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"acls__user": request.user.user.pk}
        )

    @filter_queryset_for(models.Permission)
    def filter_queryset_for_permission(self, queryset, request):
        return self.generic_own_and_admin(
            request, queryset, lambda: {"roles__acls__user": request.user.user.pk}
        )

    @filter_queryset_for(models.ACL)
    def filter_queryset_for_acl(self, queryset, request):
        return self.generic_own_and_admin(request, queryset, none=True)


class Union(BaseVisibility):
    """Union result of a list of configured visibility classes."""

    visibility_classes = []

    def filter_queryset(self, model, queryset, request):
        result_queryset = None
        for visibility_class in self.visibility_classes:
            class_result = visibility_class().filter_queryset(model, queryset, request)
            if result_queryset is None:
                result_queryset = class_result
            else:
                result_queryset = result_queryset.union(class_result)

        if result_queryset is not None:
            queryset = queryset.filter(pk__in=result_queryset.values("pk"))

        return queryset
