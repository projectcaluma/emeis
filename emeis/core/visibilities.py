import inspect

from django.core.exceptions import ImproperlyConfigured

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
    ... from emeis.core.models import User, Scope
    ...
    ...
    ... class CustomVisibility(BaseVisibility):
    ...     @filter_queryset_for(User)
    ...     def filter_queryset_for_all(self, queryset, request):
    ...         return queryset.filter(created_by_user=request.user.username)
    ...
    ...     @filter_queryset_for(Scope)
    ...     def filter_queryset_for_form(self, queryset, request):
    ...         return queryset.exclude(slug='protected-form')
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
