# Extending and embedding Emeis

Emeis is used ideally as a stand-alone microservice. However, it also can be used
as a Django app. When using Emeis as a standalone app, you can mount your own
files into the container  and point to them via environment variables.


## Extension points

For customization some clear extension points are defined. In case a customization is needed
where no extension point is defined, best [open an issue](https://github.com/projectcaluma/caluma/issues/new) for discussion.

### Visibility classes

The visibility part defines what you can see at all. Anything you cannot see, you're implicitly also not allowed to modify. The visibility classes define what you see depending on your roles, permissions, etc. Building on top of this follow the permission classes (see below) that define what you can do with the data you see.

Visibility classes are configured as `VISIBILITY_CLASSES`.

Following pre-defined classes are available:
* `emeis.core.visibilities.Any`: Allow any user without any filtering
* `emeis.core.visibilities.Union`: Union result of a list of configured visibility classes. May only be used as base class.
* `emeis.user.visibilities.OwnAndAdmin`: Only show data that belongs to the current user. For admin show all data

In case this default classes do not cover your use case, it is also possible to create your custom
visibility class defining per node how to filter.

Example:
```python
from emeis.core.visibilities import BaseVisibility, filter_queryset_for
from emeis.core.models import BaseModel, Scope


class CustomVisibility(BaseVisibility):
    @filter_queryset_for(BaseModel)
    def filter_queryset_for_all(self, queryset, request):
        return queryset.filter(created_by_user=request.user.username)
    @filter_queryset_for(Scope)
    def filter_queryset_for_scope(self, queryset, request):
        return queryset.exclude(slug='protected-scope')
```

Arguments:
* `queryset`: [Queryset](https://docs.djangoproject.com/en/2.1/ref/models/querysets/) of specific node type
* `request`: holds the [http request](https://docs.djangoproject.com/en/1.11/ref/request-response/#httprequest-objects)

Save your visibility module as `visibilities.py` and inject it as Docker volume to path `/app/caluma/extensions/visibilities.py`,

Afterwards you can configure it in `VISIBILITY_CLASSES` as `emeis.extensions.visibilities.CustomVisibility`.

### Permission classes

Permission classes define who may perform which data mutation. Such can be configured as `PERMISSION_CLASSES`.

Following pre-defined classes are available:
* `emeis.core.permissions.AllowAny`: allow any users to perform any mutation.

In case this default classes do not cover your use case, it is also possible to create your custom
permission class defining per mutation and mutation object what is allowed.

Example:
```python
from emeis.core.permissions import BasePermission, object_permission_for, permission_for
from emeis.core.models import BaseModel, User

class CustomPermission(BasePermission):
    @permission_for(BaseModel)
    def has_permission_default(self, request):
        # change default permission to False when no more specific
        # permission is defined.
        return False

    @permission_for(User)
    def has_permission_for_user(self, request):
        return True

    @object_permission_for(User)
    def has_object_permission_for_user(self, request, instance):
        return request.user.username == 'admin'
```

Arguments:
* `request`: holds the [http request](https://docs.djangoproject.com/en/1.11/ref/request-response/#httprequest-objects)
* `instance`: instance being edited by specific request

Save your permission module as `permissions.py` and inject it as Docker volume to path `/app/caluma/extensions/permissions.py`,

Afterwards you can configure it in `PERMISSION_CLASSES` as `emeis.extensions.permissions.CustomPermission`.

### Data validation

Some times, you need to validate the data sent to Emeis in a custom way. For
example, your usernames need to be checked against an external source of truth,
or you want to ensure usernames are lowercase.

For this, you can use the `EMEIS_VALIDATION_CLASSES` setting. The settings is a
list of strings that you can fill in via environment variable (comma separated
list of class names).

Here's an example validator class that ensures the username is lower case.

```python
from emeis.core.models import User
from emeis.core.validation import EmeisBaseValidator, validator_for
class LowercaseUsername(EmeisBaseValidator):
    @validator_for(User)
    def lowercase_username(self, data):
        data["username"] = data["username"].lower()
        return data
```

The `@validator_for` decorator telle Emeis that the method shall be called
when a `User` is modified. The data passed in is already parsed and validated
by Emeis, and it is expected that the method returns a `dict` with a compatible
structure. You may also `raise ValidationError("some message")` if you don't
want the validation to succeed.


### OIDC User factory

Especially when using Emeis embedded in another Django project, you need to
ensure compatibility with other components. By default, Emeis provides
a "shim" user object in it's role as an OIDC relying party (RP) that represents
the requesting user. It also points to the user model that stores that user
in the database. Other projects may have other requirements however.

Therefore, you can define a custom `EMEIS_OIDC_USER_FACTORY`. The setting is a string
that points to a callable, which is expected to return an OIDC user object. By
default it points to `emeis.oidc_auth.authentication.OIDCUser`.

The factory is called with two arguments: First, the username, and second,
a python dictionary containing the OIDC claims:

```python
    user_factory(username, claims)
```

The resulting object is expected to provide the following properties:
* `username` - returns the username.
* `user` - returns the user database model
* `is_authenticated` - Boolean that should always be `True`

You may extend the object  as you please, for example by providing shortcuts
to data you need (such as visible Emeis claims, etc).
