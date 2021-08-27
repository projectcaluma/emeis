# Extending and embedding Emeis

Emeis is used ideally as a stand-alone microservice. However, it also can be used
as a Django app. When using Emeis as a standalone app, you can mount your own
configuration / customisation files into the container and point to them via environment variables.

For customization some clear extension points are defined. In case a
customization is needed where no extension point is defined, best
[open an issue](https://github.com/projectcaluma/caluma/issues/new) for discussion.

## Extension points

Emeis uses
[Django-Generic-API-Permissions (DGAP)](https://github.com/adfinis-sygroup/django-generic-api-permissions)
to provide customizable visibility, permission, and validation.

each of those aspects is configured the same way: A settings points to one or
more classes that you need to write. Each of those classes contains one or more
methods to configure the given aspect.

Here, we only explain this in a very short version. Read the DGAP documentation linked above
for details.


### Visibility

Visibility defines what a user can see.

```python
# Put the fully qualified name of the class into the settings
# under `EMEIS_VISIBILITY_CLASSES`.
# For example, if you mount this under /app/emeis/custom/visibilities.py,
# set EMEIS_VISIBILITY_CLASSES to 'emeis.custom.visibilities.MyCustomVisibilities'

from generic_permissions.visibilities import filter_queryset_for
from emeis.core.models import BaseModel
class MyCustomVisibilities:
    """Custom visibilities:

    * Scopes are visible to everyone
    * All other objects are only visible to their respective creators
    """
    @filter_queryset_for(BaseModel)
    def show_only_mine(self, queryset, request):
        return queryset.filter(created_by_user=request.user.username)

    @filter_queryset_for(Scope)
    def filter_scopes(self, queryset, request):
        return queryset

```


### Permissions

Permissions define what a user can do with the data that the visibilities allow
them to see.

```python
# Put the fully qualified name of the class into the settings
# under `EMEIS_PERMISSION_CLASSES`.
# For example, if you mount this under /app/emeis/custom/permissions.py,
# set EMEIS_PERMISSION_CLASSES to 'emeis.custom.permissions.CustomPermission'
from generic_permissions.permissions import permission_for, object_permission_for

class CustomPermission:
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

### Validation

You can add your custom validation methods to Emeis in a similar manner.

For this, you can use the `EMEIS_VALIDATION_CLASSES` setting. The settings is a
list of strings that you can fill in via environment variable (comma separated
list of class names).

Here's an example validator class that ensures the username is lower case.

```python
# Put the fully qualified name of the class into the settings
# under `EMEIS_VALIDATION_CLASSES`.
# For example, if you mount this under /app/emeis/custom/validation.py,
# set EMEIS_VALIDATION_CLASSES to 'emeis.custom.validation.LowercaseUsername'
from emeis.core.models import User
from emeis.core.validation import EmeisBaseValidator, validator_for
class LowercaseUsername:
    @validator_for(User)
    def lowercase_username(self, data, context):
        data["username"] = data["username"].lower()
        return data
```


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
