import json

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from emeis.core.models import ACL, Scope


def _replace_in_text(in_str, **kwargs):
    if type(in_str) == dict:
        return {k: _replace_in_text(v, **kwargs) for k, v in in_str.items()}
    for key, val in kwargs.items():
        in_str = in_str.replace(f"${key}", str(val))
    return in_str


def _replace_in_args(cmd_args, user, role, scope):
    if "$role" in cmd_args:
        role_idx = cmd_args.index("$role")
        cmd_args[role_idx] = str(role.pk)
    if "$user" in cmd_args:
        user_idx = cmd_args.index("$user")
        cmd_args[user_idx] = str(user.username)
    if "$scope" in cmd_args:
        scope_idx = cmd_args.index("$scope")
        cmd_args[scope_idx] = str(scope.pk)
    return cmd_args


@pytest.mark.parametrize(
    "cmd_args, expect_out, expect_err, expect_exc",
    [
        ([], "", "", "Error: the following arguments are required: --name/-n"),
        (
            ["--name", "foo", "--user", "foo"],
            "",
            "If you pass --user, you must also pass --role",
            "",
        ),
        (
            ["--name", "foo", "--role", "foo"],
            "",
            "If you pass --role, you must also pass --user",
            "",
        ),
    ],
)
def test_param_validation(
    transactional_db,
    capsys,
    cmd_args,
    expect_out,
    expect_err,
    expect_exc,
    role,
    user,
    scope,
):
    _replace_in_args(cmd_args, user=user, role=role, scope=scope)

    if expect_exc:
        with pytest.raises(CommandError) as exc:
            call_command("create_scope", *cmd_args)

        exc_msg = "".join(exc.value.args)
        assert expect_exc.strip() == exc_msg.strip()

    else:
        call_command("create_scope", *cmd_args)
        stdout, stderr = capsys.readouterr()
        assert stdout.strip() == expect_out.strip()
        assert stderr.strip() == expect_err.strip()


@pytest.mark.parametrize(
    "cmd_args, expect_out, expect_err",
    [
        (["--name", "foobar"], "Scope created: id=$new_scope", ""),
        (
            ["--name", "foobar", "--user", "$user", "--role", "$role"],
            (
                "ACL for new scope created: user=$user, role=$role\n"
                "Scope created: id=$new_scope\n"
            ),
            "",
        ),
        (
            [
                "--name",
                '{"de": "Name DE", "en": "Name EN"}',
                "--user",
                "$user",
                "--role",
                "$role",
            ],
            (
                "ACL for new scope created: user=$user, role=$role\n"
                "Scope created: id=$new_scope\n"
            ),
            "",
        ),
        (
            ["--name", "foobar", "--user", "$user", "--role", "$role", "--json-out"],
            {"scope_id": "$new_scope", "acl_id": "$new_acl"},
            "",
        ),
        (
            [
                "--name",
                "foobar",
                "--user",
                "$user",
                "--role",
                "$role",
                "--parent",
                "$scope",
                "--json-out",
            ],
            {
                "scope_id": "$new_scope",
                "acl_id": "$new_acl",
                "parent_scope_id": "$scope",
            },
            "",
        ),
        (
            [
                "--name",
                "foobar",
                "--user",
                "$user",
                "--role",
                "$role",
                "--parent",
                "f8f635d7-dcc9-4114-838b-b63e2584f686",
                "--json-out",
            ],
            "",
            "Parent scope with given ID not found: f8f635d7-dcc9-4114-838b-b63e2584f686",
        ),
    ],
)
def test_create_success(
    transactional_db, capsys, cmd_args, expect_out, expect_err, role, user, scope, acl
):
    _replace_in_args(cmd_args, user=user, role=role, scope=scope)
    call_command("create_scope", *cmd_args)

    new_scope = Scope.objects.all().order_by("created_at").last()
    new_acl = ACL.objects.all().order_by("created_at").last()

    def replace_expectations(in_str):
        return _replace_in_text(
            in_str,
            scope=scope.pk,
            role=role.pk,
            user=user.username,
            new_scope=new_scope.pk,
            new_acl=new_acl.pk,
        )

    expect_err = replace_expectations(expect_err)
    expect_out = replace_expectations(expect_out)

    if not expect_err:
        # Check that a scope has indeed been created
        assert new_scope != scope

    stdout, stderr = capsys.readouterr()
    if type(expect_out) == dict:
        assert json.loads(stdout) == expect_out
    else:
        assert stdout.strip() == expect_out.strip()

    assert stderr.strip() == expect_err.strip()
