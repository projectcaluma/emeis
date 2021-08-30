import json

from django.core.management.base import BaseCommand

from emeis.core.models import ACL, Role, Scope, User
from emeis.core.utils import rebuild_mptt_model


class Command(BaseCommand):
    """Create an Emeis scope."""

    help = "Create an Emeis scope."

    def add_arguments(self, parser):
        parser.add_argument(
            "--parent",
            "-p",
            dest="parent",
            type=str,
            required=False,
            help="ID of parent scope. If not given, the new scope will be a top-level entity",
        )
        parser.add_argument(
            "--user",
            "-u",
            dest="user",
            type=str,
            required=False,
            help="Username to assign to the scope. User must exist. Only works with --role",
        )
        parser.add_argument(
            "--role",
            "-r",
            dest="role",
            type=str,
            required=False,
            help="Role to assign user. Only works with --user",
        )
        parser.add_argument(
            "--name",
            "-n",
            dest="name",
            type=str,
            required=True,
            help="Name of the new scope. Can be either a text, or a JSON object for a multilingual name",
        )
        parser.add_argument(
            "--json-out",
            dest="json_out",
            required=False,
            default=False,
            action="store_true",
            help="If given, output will be JSON instead of text. Useful for scripting",
        )

    def handle(self, *args, **options):
        out_info = {}
        try:
            parent = (
                Scope.objects.get(pk=options["parent"]) if options["parent"] else None
            )
            if parent:
                out_info["parent_scope_id"] = str(parent.pk)
        except Scope.DoesNotExist:
            self.stderr.write(
                f"Parent scope with given ID not found: {options['parent']}"
            )
            return

        if options["user"] and not options["role"]:
            self.stderr.write("If you pass --user, you must also pass --role")
            return
        elif options["role"] and not options["user"]:
            self.stderr.write("If you pass --role, you must also pass --user")
            return

        if options["name"].startswith("{"):
            options["name"] = json.loads(options["name"])

        new_scope = Scope.objects.create(name=options["name"], parent=parent)
        rebuild_mptt_model(Scope)
        out_info["scope_id"] = str(new_scope.pk)

        if options["user"]:
            user = User.objects.get(username=options["user"])
            role = Role.objects.get(pk=options["role"])
            new_acl = ACL.objects.create(user=user, role=role, scope=new_scope)
            out_info["acl_id"] = str(new_acl.pk)

        if options["json_out"]:
            self.stdout.write(json.dumps(out_info, indent=4))
        else:
            # string output
            if options["user"]:
                self.stdout.write(
                    f"ACL for new scope created: user={options['user']}, role={role.pk}"
                )
            self.stdout.write(f"Scope created: id={new_scope.pk}")
        self.stdout.write("\n")
