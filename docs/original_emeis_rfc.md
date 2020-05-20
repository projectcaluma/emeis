## Rationale

In Projects with rather complex ACL structures, the ACL model of Keycloak (our mainly
used OIDC provider) doesn't cover all our needs. ACLs in Keycloak are structured like this:

 - A user MAY be member of multiple groups
 - A user MAY have multiple roles
 - A user CAN'T have different roles in different groups

We have usecases, where it's important to define roles of a user per group membership. Additionally we need the possibility to create a group hierarchy, where a group MAY have multiple sub-groups.

So our requirements are like this:

 - A user MAY be member of multiple groups
 - A user MAY have multiple roles in a group
 - A user MAY have different roles in different groups
 - Groups MAY have one or multiple sub-groups

In order not to reimplement these requirements in every project that needs user
management, we want a generic user management solution.

## Goal

Our goal is to implement an external user management service to hold and provide ACLs.

This service should not act as an OIDC provider, but hold augmenting data about the
users, a group hierarchy and roles. It should play nicely with any OIDC provider.

The usefullness of this service is by no means limited to Caluma. It will be a generic service to manage ACLs.

It should provide a web API following the json-api spec.

## Illustration of a request

![diagram](https://user-images.githubusercontent.com/1833932/81042900-76b2b400-8eb1-11ea-91e6-516d3ef59e6a.png)

## Models

### Common fields

All models share a common set of fields:

 - `created_at`
 - `created_by`
 - `modified_at`
 - `modified_by`

### Design considerations

`roles` are considered configuration and thus have a `slug` primary key. All other
models are considered runtime data and have a UUID primary key.

### User

| Column       | Type             | Comment     |
| ------------ | ---------------- | ----------- |
| `UUID`       | UUID             | primary key |
| `username`   | Char             | unique      |
| `name`       | Char             |             |
| `surname`    | Char             |             |
| `email`      | Char             |             |
| `phone`      | Char             |             |
| `disabled`   | Bool             |             |
| `language`   | Choice           |             |
| `address`    | Char             |             |
| `city`       | LocalizedField   |             |
| `zip`        | Char             |             |
| `meta`       | JSON             |             |
| `active`      | bool                  |            |
| `acls`       | reverse relation |             |

We want to provide a useful set of properties, sufficient for most use cases and
extensible through a `meta` field.

The selection of fields on the `User` model will be subject to further discussions.

### Scope

| Column        | Type                  | Comment    |
| ------------- | --------------------- | ---------- |
| `UUID`        | UUID                  | primary key|
| `name`        | LocalizedField        |            |
| `description` | LocalizedField        |            |
| `parent`      | self ForeignKey       |            |
| `children`       | self reverse relation |            |
| `acls`        | reverse relation      |            |

### Role

| Column        | Type             | Comment     |
| ------------- | ---------------- | ----------- |
| `slug`        | Char             | primary key |
| `name`        | LocalizedField   |             |
| `description` | LocalizedField   |             |
|`permissions`      | many2many ||
| `acls`        | reverse relation |             |

### Permission

| Column        | Type             | Comment     |
| ------------- | ---------------- | ----------- |
| `slug`        | Char             | primary key |
| `name`        | LocalizedField   |             |
| `description` | LocalizedField   |             |
|`roles`      | many2many ||

### ACL

| Column  | Type       | Comment     |
| ------- | ---------- | ----------- |
| `UUID`  | UUID       | primary key |
| `user`  | ForeignKey |             |
| `scope` | ForeignKey |             |
| `role`  | ForeignKey |             |

Unique together `user`, `scope`, `role`.

## API

The exact design of the API and its capabilities will be consolidated in close
collaboration with the frontend engineers.

### /user list

List and filter users

### /user retrieve

Retrieve information about a user.

### /user update

Update existing user.

### /user delete

Delete an existing user.

### /scope list

List and filter scopes

### /scope retrieve

Retrieve information about a scope.

### /scope create

Create a new scope.

### /scope update

Update existing scope.

### /scope delete

Delete an existing scope.

### /permission list

List and filter permissions

### /scope retrieve

Retrieve information about a permission.

### /permission create

Create a new permission.

### /permission update

Update existing permission.

### /permission delete

Delete an existing permission.

### /role list

List and filter roles.

### /role retrieve

Retrieve information about a role.

### /role create

Create a new role.

### /role delete

Delete an existing role.

### /acl list

List and filter ACLs

### /acl retrieve

Retrieve information about an ACL.

### /acl create

Create a new ACL.

### /acl delete

Delete an existing ACL.


## Note on user deletion

Most modern systems do not allow for deleting a `user` instance. This, however, is not
compliant with swiss data protection law and GDPR.

We should design the system in a way that allows for deletion of `user` instances and
also provide an endpoint for that.

Additionally we should provide an `active` flag on `user` instances, thus leaving it up
to the consuming project, how to handle this.


## Data management

There will be a dedicated frontend or tools for building such with ember.js. For a
quick PoC it is discussed to use Django admin. We agreed upon the importance of an
attractive UI.

### Workflow

In order to configure a new user, following steps will be necessary:

1. Creating the user in the OIDC provider.
2. Making a random request with a valid token to our user management. This will create
    the user there.
3. Configuring metadata and ACLs of that user in the user management.

Alternative workflow:

1. Creating the user in the OIDC provider.
2. Creating and configuring the user and its memberships in the user management
3. On the first request, match the email address (or any other unique property) in order to link the OIDC user with the already existing. If no match has been found, create a new user (above workflow applies).

## Permissions and Visibilities

We need fine-grained control over permissions and visibilities inside the user
management. For this it would be sensible to implement an approach similar to Caluma
with its permission and visibility classes.

Some default classes should be provided. For example:

 - `permissions.AllowGroupAdmins` --> Allow group mutations for users with role
   `group_admin`.
 - `visibilities.OwnGroups` --> Allow fetching information about groups the requesting
   user is a member of.

## Bootstrapping

In order to get up and running with an admin user, following solution is proposed:

If a new user makes a request (it exists in the OIDC provider, but not in the user management system) and its email address is found in `settings.ADMINS`, it will automatically be assigned an admin group membership and role.

Admin group and role can be configured in the settings. Example:

```python
ADMINS = ["root@caluma.io"]

ADMIN_GROUP_UUID = "66fbabbd-f694-4951-84b2-f5415ff5f3bc"
ADMIN_ROLE_SLUG = "system_admin"
```

With these settings in place, our system makes sure, that a group with the provided UUID exists as well as a role with the provided slug. A request of a new user with the email address `root@caluma.io` will then lead to a new local user with a membership in the configured group with the configured role. Our system only cares for the PKs, all other properties of this group and role can be freely set as with any group or role.

## Integration in Caluma

The document-merge-service already supports configuring a dedicated endpoint for [fetching groups](https://github.com/adfinis-sygroup/document-merge-service/blob/fb56a42aee82f9261596f7546f52f8b9930292de/document_merge_service/api/authentication.py#L84). It will be trivial and useful to implement this in Caluma as well. That way we could very easiliy have basic support for our user management in Caluma.

For simple usecases, this could already cover all needs on the Caluma side:

![diagram_simple](https://user-images.githubusercontent.com/1833932/81044687-1756a300-8eb5-11ea-942f-1c255b6dbe30.png)

As soon as additional information is needed in Caluma (more than just the list of
groups), it still has to be queried manually in the permission extension.

--> See #1048.

## Additional functionality

 - Export data to json
 - Import data from json

## Name
We need a snappy name for this project.

### Proposal
I propose `emeis` (`[e̞ˈmis]`) as name for the new project. It is greek (εμείς) and means `we`. A quick websearch did not bring up any conflicting projects.
