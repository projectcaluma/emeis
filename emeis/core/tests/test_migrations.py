from django.db import connection
from django.db.migrations.executor import MigrationExecutor


def test_data_bootstrap(transactional_db, settings):
    executor = MigrationExecutor(connection)
    app = "emeis_core"
    migrate_from = [(app, "0001_initial")]
    migrate_to = [(app, "0002_data_bootstrap")]

    executor.migrate(migrate_from)
    old_apps = executor.loader.project_state(migrate_from).apps

    User = old_apps.get_model(app, "User")
    Scope = old_apps.get_model(app, "Scope")
    Role = old_apps.get_model(app, "Role")
    Acl = old_apps.get_model(app, "Acl")

    for model in [User, Scope, Role, Acl]:
        getattr(model, "objects").all().delete()
        assert getattr(model, "objects").count() == 0

    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)
    new_apps = executor.loader.project_state(migrate_to).apps

    # Test the new data.
    User = new_apps.get_model(app, "User")
    Scope = new_apps.get_model(app, "Scope")
    Role = new_apps.get_model(app, "Role")
    Acl = new_apps.get_model(app, "Acl")

    for model in [User, Scope, Role, Acl]:
        assert getattr(model, "objects").count() == 1

    assert User.objects.first().username == settings.ADMIN_USERNAME
    assert Role.objects.first().slug == settings.ADMIN_ROLE_SLUG
    scope = Scope.objects.first()
    assert scope.name["en"] == settings.ADMIN_SCOPE_NAME
    assert scope.tree_id == 1
