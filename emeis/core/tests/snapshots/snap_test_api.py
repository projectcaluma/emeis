# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_api_list[RoleViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT ("emeis_core_role_permissions"."role_id") AS "_prefetch_related_val_role_id", "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" IN (\'front-her-occur\', \'kid-owner-car\', \'note-act-source\', \'run-too-successful\')',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" = \'program-small\' ORDER BY "emeis_core_role"."slug" ASC',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/roles",
        "QUERY_STRING": "include=permissions",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Process truth assume popular contain commercial with. Detail race high even might.
Thing summer prevent free environment measure role later. Capital direction capital Congress doctor land prevent.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Linda Taylor", "fr": ""},
                    "slug": "front-her-occur",
                },
                "id": "front-her-occur",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Open else look tree arm responsibility week. Environmental statement bag someone them style.
Public these health team change. Tax final upon stay sing middle suggest.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Gregory Scott", "fr": ""},
                    "slug": "kid-owner-car",
                },
                "id": "kid-owner-car",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {
                        "data": [{"id": "program-small", "type": "permissions"}],
                        "meta": {"count": 1},
                    },
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                    "slug": "note-act-source",
                },
                "id": "note-act-source",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Arm serious live by itself. Project find white continue none president.
Partner area media increase meeting article. Success provide beyond seek officer player.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Timothy Malone", "fr": ""},
                    "slug": "run-too-successful",
                },
                "id": "run-too-successful",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
        ],
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Sound discover Mrs once long. Well treatment radio with Mr letter eye. Society street hair local kind debate line simple.
Treat better note everybody party. Miss south speak industry.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Denise Horton", "fr": ""},
                    "slug": "program-small",
                },
                "id": "program-small",
                "relationships": {
                    "created-by-user": {"data": None},
                    "roles": {
                        "data": [{"id": "kid-owner-car", "type": "roles"}],
                        "meta": {"count": 1},
                    },
                },
                "type": "permissions",
            }
        ],
    },
    "status": 200,
}

snapshots["test_api_list[ACLViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl"',
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" IN (\'0b0cfc07-fca8-1c95-6ab9-181d8576f4a8\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid)',
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'aba369f7-d2b2-8a90-98a0-a26feb7dc965\'::uuid, \'dad3a37a-a9d5-0688-b515-7698acfd7aee\'::uuid)',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" IN (\'form-level-clear\', \'fund-executive-most\', \'over-catch-plant\') ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'fund-executive-most\'',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'over-catch-plant\'',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'0b0cfc07-fca8-1c95-6ab9-181d8576f4a8\'::uuid',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'form-level-clear\'',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/acls",
        "QUERY_STRING": "include=user%2Cscope%2Crole",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "created-by-user": {"data": None},
                    "role": {"data": {"id": "fund-executive-most", "type": "roles"}},
                    "scope": {
                        "data": {
                            "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                            "type": "scopes",
                        }
                    },
                    "user": {
                        "data": {
                            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                            "type": "users",
                        }
                    },
                },
                "type": "acls",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                },
                "id": "04adb4e2-f055-c978-c9bb-101ee1bc5cd4",
                "relationships": {
                    "created-by-user": {"data": None},
                    "role": {"data": {"id": "over-catch-plant", "type": "roles"}},
                    "scope": {
                        "data": {
                            "id": "dad3a37a-a9d5-0688-b515-7698acfd7aee",
                            "type": "scopes",
                        }
                    },
                    "user": {
                        "data": {
                            "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
                            "type": "users",
                        }
                    },
                },
                "type": "acls",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                },
                "id": "336311a0-1618-4326-ddbd-d61edd4eeb52",
                "relationships": {
                    "created-by-user": {"data": None},
                    "role": {"data": {"id": "form-level-clear", "type": "roles"}},
                    "scope": {
                        "data": {
                            "id": "aba369f7-d2b2-8a90-98a0-a26feb7dc965",
                            "type": "scopes",
                        }
                    },
                    "user": {
                        "data": {
                            "id": "0b0cfc07-fca8-1c95-6ab9-181d8576f4a8",
                            "type": "users",
                        }
                    },
                },
                "type": "acls",
            },
        ],
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Tell save term few military feeling. Avoid generation nearly laugh. Human great region administration bar rate threat.
Open should upon few play. Seven knowledge property already better.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Wayne Key", "fr": ""},
                    "slug": "form-level-clear",
                },
                "id": "form-level-clear",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Truth deep public these. View mind stop serve tax final. Stay sing middle suggest.
Even yourself responsibility sound air mission value. Character last guy. Plan contain task various few.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Michael Arias", "fr": ""},
                    "slug": "fund-executive-most",
                },
                "id": "fund-executive-most",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Range laugh whether reduce remain summer international. Official care or conference. Risk against capital factor.
Trade for brother. Upon apply edge summer movie.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Beverly Davis", "fr": ""},
                    "slug": "over-catch-plant",
                },
                "id": "over-catch-plant",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": "Ago get want middle. Whose scientist draw free property consider rather. Have director true force.",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Stephanie Porter", "fr": ""},
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": "Form leader fund task believe oil. Itself close again affect ok window church. Claim interview participant call strategy.",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Dr. Jose Campbell", "fr": ""},
                },
                "id": "aba369f7-d2b2-8a90-98a0-a26feb7dc965",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": "Beyond seek officer player possible issue. Trial population standard. After away control expert without assume grow back.",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Mary White", "fr": ""},
                },
                "id": "dad3a37a-a9d5-0688-b515-7698acfd7aee",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "karen47@example.com",
                    "first-name": "Jennifer",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Johnson",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "kdowns",
                    "zip": None,
                },
                "id": "0b0cfc07-fca8-1c95-6ab9-181d8576f4a8",
                "relationships": {
                    "acls": {
                        "data": [
                            {
                                "id": "336311a0-1618-4326-ddbd-d61edd4eeb52",
                                "type": "acls",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "kennethgarcia@example.org",
                    "first-name": "Amanda",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Gallagher",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "mark48",
                    "zip": None,
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "acls": {
                        "data": [
                            {
                                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                                "type": "acls",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "dmiller@example.org",
                    "first-name": "Heather",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Marsh",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "jackellis",
                    "zip": None,
                },
                "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
                "relationships": {
                    "acls": {
                        "data": [
                            {
                                "id": "04adb4e2-f055-c978-c9bb-101ee1bc5cd4",
                                "type": "acls",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_list[PermissionViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission"',
        'SELECT ("emeis_core_role_permissions"."permission_id") AS "_prefetch_related_val_permission_id", "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" IN (\'front-her-occur\', \'note-act-source\', \'run-too-successful\') ORDER BY "emeis_core_role"."slug" ASC',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/permissions",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Erin Scott", "fr": ""},
                    "slug": "note-act-source",
                },
                "id": "note-act-source",
                "relationships": {
                    "created-by-user": {"data": None},
                    "roles": {"data": [], "meta": {"count": 0}},
                },
                "type": "permissions",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Arm serious live by itself. Project find white continue none president.
Partner area media increase meeting article. Success provide beyond seek officer player.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Timothy Malone", "fr": ""},
                    "slug": "run-too-successful",
                },
                "id": "run-too-successful",
                "relationships": {
                    "created-by-user": {"data": None},
                    "roles": {"data": [], "meta": {"count": 0}},
                },
                "type": "permissions",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Process truth assume popular contain commercial with. Detail race high even might.
Thing summer prevent free environment measure role later. Capital direction capital Congress doctor land prevent.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Linda Taylor", "fr": ""},
                    "slug": "front-her-occur",
                },
                "id": "front-her-occur",
                "relationships": {
                    "created-by-user": {"data": None},
                    "roles": {"data": [], "meta": {"count": 0}},
                },
                "type": "permissions",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[ScopeViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" ORDER BY "emeis_core_scope"."tree_id" ASC, "emeis_core_scope"."lft" ASC'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/scopes",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Pamela Horton", "fr": ""},
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Bank arm serious live by itself. Project find white continue none president. Idea eye plan third program.
Son success provide beyond. Officer player possible issue ahead suffer.""",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Rebecca Gonzalez", "fr": ""},
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Free environment measure role later now over.
Can bed notice range. Minute can second prove every check official. Stay culture create risk.
Daughter single product trade.""",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Lorraine Reynolds", "fr": ""},
                },
                "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_list[UserViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user"',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid, \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/users",
        "QUERY_STRING": "include=acls",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": [
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "kennethgarcia@example.org",
                    "first-name": "Amanda",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Gallagher",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "mark48",
                    "zip": None,
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "acls": {"data": [], "meta": {"count": 0}},
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "fieldsjanice@example.net",
                    "first-name": "Natalie",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Hurst",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "admin",
                    "zip": None,
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "acls": {"data": [], "meta": {"count": 0}},
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "dmiller@example.org",
                    "first-name": "Heather",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Marsh",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "jackellis",
                    "zip": None,
                },
                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                "relationships": {
                    "acls": {"data": [], "meta": {"count": 0}},
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "vgarcia@example.com",
                    "first-name": "Nicole",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Ortega",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "brucegutierrez",
                    "zip": None,
                },
                "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                "relationships": {
                    "acls": {"data": [], "meta": {"count": 0}},
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
        ]
    },
    "status": 200,
}

snapshots["test_api_detail[ACLViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" IN (\'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid)',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" IN (\'fund-executive-most\') ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'fund-executive-most\'',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/acls/f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
        "QUERY_STRING": "include=user%2Cscope%2Crole",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "created-by-user": {"data": None},
                "role": {"data": {"id": "fund-executive-most", "type": "roles"}},
                "scope": {
                    "data": {
                        "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                        "type": "scopes",
                    }
                },
                "user": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "users",
                    }
                },
            },
            "type": "acls",
        },
        "included": [
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": """Truth deep public these. View mind stop serve tax final. Stay sing middle suggest.
Even yourself responsibility sound air mission value. Character last guy. Plan contain task various few.""",
                        "fr": "",
                    },
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Michael Arias", "fr": ""},
                    "slug": "fund-executive-most",
                },
                "id": "fund-executive-most",
                "relationships": {
                    "created-by-user": {"data": None},
                    "permissions": {"data": [], "meta": {"count": 0}},
                },
                "type": "roles",
            },
            {
                "attributes": {
                    "created-at": "2017-05-21T00:00:00Z",
                    "description": {
                        "de": "",
                        "en": "Ago get want middle. Whose scientist draw free property consider rather. Have director true force.",
                        "fr": "",
                    },
                    "level": 0,
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "name": {"de": "", "en": "Stephanie Porter", "fr": ""},
                },
                "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                "relationships": {
                    "created-by-user": {"data": None},
                    "parent": {"data": None},
                },
                "type": "scopes",
            },
            {
                "attributes": {
                    "address": None,
                    "city": {"de": "", "en": "", "fr": ""},
                    "created-at": "2017-05-21T00:00:00Z",
                    "date-joined": "2017-05-21T00:00:00Z",
                    "email": "kennethgarcia@example.org",
                    "first-name": "Amanda",
                    "is-active": True,
                    "language": "en",
                    "last-name": "Gallagher",
                    "meta": {},
                    "modified-at": "2017-05-21T00:00:00Z",
                    "phone": None,
                    "username": "mark48",
                    "zip": None,
                },
                "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                "relationships": {
                    "acls": {
                        "data": [
                            {
                                "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
                                "type": "acls",
                            }
                        ],
                        "meta": {"count": 1},
                    },
                    "created-by-user": {"data": None},
                },
                "type": "users",
            },
        ],
    },
    "status": 200,
}

snapshots["test_api_detail[PermissionViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" WHERE "emeis_core_permission"."slug" = \'note-act-source\'',
        'SELECT ("emeis_core_role_permissions"."permission_id") AS "_prefetch_related_val_permission_id", "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" IN (\'note-act-source\') ORDER BY "emeis_core_role"."slug" ASC',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/permissions/note-act-source",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {"data": None},
                "roles": {"data": [], "meta": {"count": 0}},
            },
            "type": "permissions",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[RoleViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'note-act-source\'',
        'SELECT ("emeis_core_role_permissions"."role_id") AS "_prefetch_related_val_role_id", "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" IN (\'note-act-source\')',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/roles/note-act-source",
        "QUERY_STRING": "include=permissions",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {"data": None},
                "permissions": {"data": [], "meta": {"count": 0}},
            },
            "type": "roles",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[ScopeViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid'
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/scopes/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "level": 0,
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Pamela Horton", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "created-by-user": {"data": None},
                "parent": {"data": None},
            },
            "type": "scopes",
        }
    },
    "status": 200,
}

snapshots["test_api_detail[UserViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "CONTENT_TYPE": "application/octet-stream",
        "PATH_INFO": "/api/v1/users/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "include=acls",
        "REQUEST_METHOD": "GET",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "address": None,
                "city": {"de": "", "en": "", "fr": ""},
                "created-at": "2017-05-21T00:00:00Z",
                "date-joined": "2017-05-21T00:00:00Z",
                "email": "kennethgarcia@example.org",
                "first-name": "Amanda",
                "is-active": True,
                "language": "en",
                "last-name": "Gallagher",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "phone": None,
                "username": "mark48",
                "zip": None,
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "acls": {"data": [], "meta": {"count": 0}},
                "created-by-user": {"data": None},
            },
            "type": "users",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[ACLViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'fund-executive-most\'',
        'SELECT (1) AS "a" FROM "emeis_core_acl" WHERE ("emeis_core_acl"."role_id" = \'fund-executive-most\' AND "emeis_core_acl"."scope_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid AND "emeis_core_acl"."user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid AND NOT ("emeis_core_acl"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid))  LIMIT 1',
        'UPDATE "emeis_core_acl" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user_id" = NULL, "meta" = \'{}\', "user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, "scope_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, "role_id" = \'fund-executive-most\' WHERE "emeis_core_acl"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "432",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/acls/f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "created-by-user": {"data": None},
                "role": {"data": {"id": "fund-executive-most", "type": "roles"}},
                "scope": {
                    "data": {
                        "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                        "type": "scopes",
                    }
                },
                "user": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "users",
                    }
                },
            },
            "type": "acls",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[PermissionViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" WHERE "emeis_core_permission"."slug" = \'note-act-source\'',
        'SELECT ("emeis_core_role_permissions"."permission_id") AS "_prefetch_related_val_permission_id", "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" IN (\'note-act-source\') ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT (1) AS "a" FROM "emeis_core_permission" WHERE ("emeis_core_permission"."slug" = \'note-act-source\' AND NOT ("emeis_core_permission"."slug" = \'note-act-source\'))  LIMIT 1',
        """UPDATE "emeis_core_permission" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user_id" = NULL, "meta" = \'{}\', "name" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.\',\'\',\'\']) WHERE "emeis_core_permission"."slug" = \'note-act-source\'""",
        'SELECT "emeis_core_role"."slug" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" = \'note-act-source\' ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" = \'note-act-source\' ORDER BY "emeis_core_role"."slug" ASC',
    ],
    "request": {
        "CONTENT_LENGTH": "548",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/permissions/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {"data": None},
                "roles": {"data": [], "meta": {"count": 0}},
            },
            "type": "permissions",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[RoleViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'note-act-source\'',
        'SELECT (1) AS "a" FROM "emeis_core_role" WHERE ("emeis_core_role"."slug" = \'note-act-source\' AND NOT ("emeis_core_role"."slug" = \'note-act-source\'))  LIMIT 1',
        """UPDATE "emeis_core_role" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user_id" = NULL, "meta" = \'{}\', "name" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.\',\'\',\'\']) WHERE "emeis_core_role"."slug" = \'note-act-source\'""",
        'SELECT "emeis_core_permission"."slug" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'note-act-source\'',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'note-act-source\'',
    ],
    "request": {
        "CONTENT_LENGTH": "548",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/roles/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {"data": None},
                "permissions": {"data": [], "meta": {"count": 0}},
            },
            "type": "roles",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[ScopeViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        """UPDATE "emeis_core_scope" SET "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user_id" = NULL, "meta" = \'{}\', "name" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Pamela Horton\',\'\',\'\']), "description" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.\',\'\',\'\']), "parent_id" = NULL WHERE "emeis_core_scope"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid""",
    ],
    "request": {
        "CONTENT_LENGTH": "516",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/scopes/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "level": 0,
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Pamela Horton", "fr": ""},
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "created-by-user": {"data": None},
                "parent": {"data": None},
            },
            "type": "scopes",
        }
    },
    "status": 200,
}

snapshots["test_api_patch[UserViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT (1) AS "a" FROM "emeis_core_user" WHERE ("emeis_core_user"."username" = \'mark48\' AND NOT ("emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid))  LIMIT 1',
        'UPDATE "emeis_core_user" SET "password" = \'_nNx5pap05\', "last_login" = \'2021-07-20T12:00:00+00:00\'::timestamptz, "created_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "modified_at" = \'2017-05-21T00:00:00+00:00\'::timestamptz, "created_by_user_id" = NULL, "meta" = \'{}\', "username" = \'mark48\', "first_name" = \'Amanda\', "last_name" = \'Gallagher\', "email" = \'kennethgarcia@example.org\', "phone" = NULL, "language" = \'en\', "address" = NULL, "city" = hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'\',\'\',\'\']), "zip" = NULL, "is_active" = true, "date_joined" = \'2017-05-21T00:00:00+00:00\'::timestamptz WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "499",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/users/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "PATCH",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "address": None,
                "city": {"de": "", "en": "", "fr": ""},
                "created-at": "2017-05-21T00:00:00Z",
                "date-joined": "2017-05-21T00:00:00Z",
                "email": "kennethgarcia@example.org",
                "first-name": "Amanda",
                "is-active": True,
                "language": "en",
                "last-name": "Gallagher",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "phone": None,
                "username": "mark48",
                "zip": None,
            },
            "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
            "relationships": {
                "acls": {"data": [], "meta": {"count": 0}},
                "created-by-user": {"data": None},
            },
            "type": "users",
        }
    },
    "status": 200,
}

snapshots["test_api_destroy[ACLViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
        'DELETE FROM "emeis_core_acl" WHERE "emeis_core_acl"."id" IN (\'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid)',
    ],
    "request": {
        "PATH_INFO": "/api/v1/acls/f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[PermissionViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" WHERE "emeis_core_permission"."slug" = \'note-act-source\'',
        'SELECT ("emeis_core_role_permissions"."permission_id") AS "_prefetch_related_val_permission_id", "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" IN (\'note-act-source\') ORDER BY "emeis_core_role"."slug" ASC',
        'DELETE FROM "emeis_core_role_permissions" WHERE "emeis_core_role_permissions"."permission_id" IN (\'note-act-source\')',
        'DELETE FROM "emeis_core_permission" WHERE "emeis_core_permission"."slug" IN (\'note-act-source\')',
    ],
    "request": {
        "PATH_INFO": "/api/v1/permissions/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[RoleViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'note-act-source\'',
        'DELETE FROM "emeis_core_role_permissions" WHERE "emeis_core_role_permissions"."role_id" IN (\'note-act-source\')',
        'DELETE FROM "emeis_core_acl" WHERE "emeis_core_acl"."role_id" IN (\'note-act-source\')',
        'DELETE FROM "emeis_core_role" WHERE "emeis_core_role"."slug" IN (\'note-act-source\')',
    ],
    "request": {
        "PATH_INFO": "/api/v1/roles/note-act-source",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[ScopeViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_scope"."id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        """
            UPDATE "emeis_core_scope"
            SET "lft" = CASE
                    WHEN "lft" > 2
                        THEN "lft" +  -2
                    ELSE "lft" END,
                "rght" = CASE
                    WHEN "rght" > 2
                        THEN "rght" +  -2
                    ELSE "rght" END
            WHERE "tree_id" = 1
              AND ("lft" > 2 OR "rght" > 2)""",
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."parent_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "emeis_core_acl" WHERE "emeis_core_acl"."scope_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "PATH_INFO": "/api/v1/scopes/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_destroy[UserViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."created_by_user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."created_by_user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."created_by_user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid) ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" WHERE "emeis_core_permission"."created_by_user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."created_by_user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
        'DELETE FROM "emeis_core_user" WHERE "emeis_core_user"."id" IN (\'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)',
    ],
    "request": {
        "PATH_INFO": "/api/v1/users/9dd4e461-268c-8034-f5c8-564e155c67a6",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "DELETE",
        "SERVER_PORT": "80",
    },
    "status": 204,
}

snapshots["test_api_create[ACLViewSet] 1"] = {
    "queries": [
        'SELECT "emeis_core_user"."password", "emeis_core_user"."last_login", "emeis_core_user"."created_at", "emeis_core_user"."modified_at", "emeis_core_user"."created_by_user_id", "emeis_core_user"."meta", "emeis_core_user"."id", "emeis_core_user"."username", "emeis_core_user"."first_name", "emeis_core_user"."last_name", "emeis_core_user"."email", "emeis_core_user"."phone", "emeis_core_user"."language", "emeis_core_user"."address", "emeis_core_user"."city", "emeis_core_user"."zip", "emeis_core_user"."is_active", "emeis_core_user"."date_joined" FROM "emeis_core_user" WHERE "emeis_core_user"."id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid',
        'SELECT "emeis_core_scope"."created_at", "emeis_core_scope"."modified_at", "emeis_core_scope"."created_by_user_id", "emeis_core_scope"."meta", "emeis_core_scope"."id", "emeis_core_scope"."name", "emeis_core_scope"."description", "emeis_core_scope"."parent_id", "emeis_core_scope"."lft", "emeis_core_scope"."rght", "emeis_core_scope"."tree_id", "emeis_core_scope"."level" FROM "emeis_core_scope" WHERE "emeis_core_scope"."id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'fund-executive-most\'',
        'SELECT (1) AS "a" FROM "emeis_core_acl" WHERE ("emeis_core_acl"."role_id" = \'fund-executive-most\' AND "emeis_core_acl"."scope_id" = \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid AND "emeis_core_acl"."user_id" = \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid)  LIMIT 1',
        'INSERT INTO "emeis_core_acl" ("created_at", "modified_at", "created_by_user_id", "meta", "id", "user_id", "scope_id", "role_id") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'ea416ed0-759d-46a8-de58-f63a59077499\'::uuid, \'{}\', \'fb0e22c7-9ac7-5679-e988-1e6ba183b354\'::uuid, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'fund-executive-most\')',
    ],
    "request": {
        "CONTENT_LENGTH": "432",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/acls",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
            },
            "id": "fb0e22c7-9ac7-5679-e988-1e6ba183b354",
            "relationships": {
                "created-by-user": {
                    "data": {
                        "id": "ea416ed0-759d-46a8-de58-f63a59077499",
                        "type": "users",
                    }
                },
                "role": {"data": {"id": "fund-executive-most", "type": "roles"}},
                "scope": {
                    "data": {
                        "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                        "type": "scopes",
                    }
                },
                "user": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "users",
                    }
                },
            },
            "type": "acls",
        }
    },
    "status": 201,
}

snapshots["test_api_create[PermissionViewSet] 1"] = {
    "queries": [
        'SELECT (1) AS "a" FROM "emeis_core_permission" WHERE "emeis_core_permission"."slug" = \'note-act-source\'  LIMIT 1',
        """INSERT INTO "emeis_core_permission" ("created_at", "modified_at", "created_by_user_id", "meta", "slug", "name", "description") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'{}\', \'note-act-source\', hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.','','']))""",
        'SELECT "emeis_core_role"."slug" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" = \'note-act-source\' ORDER BY "emeis_core_role"."slug" ASC',
        'SELECT "emeis_core_role"."created_at", "emeis_core_role"."modified_at", "emeis_core_role"."created_by_user_id", "emeis_core_role"."meta", "emeis_core_role"."slug", "emeis_core_role"."name", "emeis_core_role"."description" FROM "emeis_core_role" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_role"."slug" = "emeis_core_role_permissions"."role_id") WHERE "emeis_core_role_permissions"."permission_id" = \'note-act-source\' ORDER BY "emeis_core_role"."slug" ASC',
    ],
    "request": {
        "CONTENT_LENGTH": "548",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/permissions",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "users",
                    }
                },
                "roles": {"data": [], "meta": {"count": 0}},
            },
            "type": "permissions",
        }
    },
    "status": 201,
}

snapshots["test_api_create[RoleViewSet] 1"] = {
    "queries": [
        'SELECT (1) AS "a" FROM "emeis_core_role" WHERE "emeis_core_role"."slug" = \'note-act-source\'  LIMIT 1',
        """INSERT INTO "emeis_core_role" ("created_at", "modified_at", "created_by_user_id", "meta", "slug", "name", "description") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'9dd4e461-268c-8034-f5c8-564e155c67a6\'::uuid, \'{}\', \'note-act-source\', hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Erin Scott\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.','','']))""",
        'SELECT "emeis_core_permission"."slug" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'note-act-source\'',
        'SELECT "emeis_core_permission"."created_at", "emeis_core_permission"."modified_at", "emeis_core_permission"."created_by_user_id", "emeis_core_permission"."meta", "emeis_core_permission"."slug", "emeis_core_permission"."name", "emeis_core_permission"."description" FROM "emeis_core_permission" INNER JOIN "emeis_core_role_permissions" ON ("emeis_core_permission"."slug" = "emeis_core_role_permissions"."permission_id") WHERE "emeis_core_role_permissions"."role_id" = \'note-act-source\'',
    ],
    "request": {
        "CONTENT_LENGTH": "548",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/roles",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Far bit among again. Station story first. Team suggest traditional boy above.
Central meeting anyone remember. There today material minute ago get. Range whose scientist draw free property consider.""",
                    "fr": "",
                },
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Erin Scott", "fr": ""},
                "slug": "note-act-source",
            },
            "id": "note-act-source",
            "relationships": {
                "created-by-user": {
                    "data": {
                        "id": "9dd4e461-268c-8034-f5c8-564e155c67a6",
                        "type": "users",
                    }
                },
                "permissions": {"data": [], "meta": {"count": 0}},
            },
            "type": "roles",
        }
    },
    "status": 201,
}

snapshots["test_api_create[ScopeViewSet] 1"] = {
    "queries": [
        'SELECT MAX("emeis_core_scope"."tree_id") AS "tree_id__max" FROM "emeis_core_scope"',
        """INSERT INTO "emeis_core_scope" ("created_at", "modified_at", "created_by_user_id", "meta", "id", "name", "description", "parent_id", "lft", "rght", "tree_id", "level") VALUES (\'2017-05-21T00:00:00+00:00\'::timestamptz, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'{}\', \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Pamela Horton\',\'\',\'\']), hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.','','']), NULL, 1, 2, 1, 0)""",
    ],
    "request": {
        "CONTENT_LENGTH": "516",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/scopes",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "created-at": "2017-05-21T00:00:00Z",
                "description": {
                    "de": "",
                    "en": """Effort meet relationship far. Option program interesting station. First where during teach country talk across.
Argue move appear catch toward help wind. Material minute ago get.""",
                    "fr": "",
                },
                "level": 0,
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "name": {"de": "", "en": "Pamela Horton", "fr": ""},
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "created-by-user": {
                    "data": {
                        "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                        "type": "users",
                    }
                },
                "parent": {"data": None},
            },
            "type": "scopes",
        }
    },
    "status": 201,
}

snapshots["test_api_create[UserViewSet] 1"] = {
    "queries": [
        'SELECT (1) AS "a" FROM "emeis_core_user" WHERE "emeis_core_user"."username" = \'mark48\'  LIMIT 1',
        'INSERT INTO "emeis_core_user" ("password", "last_login", "created_at", "modified_at", "created_by_user_id", "meta", "id", "username", "first_name", "last_name", "email", "phone", "language", "address", "city", "zip", "is_active", "date_joined") VALUES (\'\', NULL, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'2017-05-21T00:00:00+00:00\'::timestamptz, \'9336ebf2-5087-d91c-818e-e6e9ec29f8c1\'::uuid, \'{}\', \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid, \'mark48\', \'Amanda\', \'Gallagher\', \'kennethgarcia@example.org\', NULL, \'en\', NULL, hstore(ARRAY[\'en\',\'de\',\'fr\'], ARRAY[\'\',\'\',\'\']), NULL, true, \'2017-05-21T00:00:00+00:00\'::timestamptz)',
        'SELECT "emeis_core_acl"."created_at", "emeis_core_acl"."modified_at", "emeis_core_acl"."created_by_user_id", "emeis_core_acl"."meta", "emeis_core_acl"."id", "emeis_core_acl"."user_id", "emeis_core_acl"."scope_id", "emeis_core_acl"."role_id" FROM "emeis_core_acl" WHERE "emeis_core_acl"."user_id" = \'f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad\'::uuid',
    ],
    "request": {
        "CONTENT_LENGTH": "499",
        "CONTENT_TYPE": "application/vnd.api+json",
        "PATH_INFO": "/api/v1/users",
        "QUERY_STRING": "",
        "REQUEST_METHOD": "POST",
        "SERVER_PORT": "80",
    },
    "response": {
        "data": {
            "attributes": {
                "address": None,
                "city": {"de": "", "en": "", "fr": ""},
                "created-at": "2017-05-21T00:00:00Z",
                "date-joined": "2017-05-21T00:00:00Z",
                "email": "kennethgarcia@example.org",
                "first-name": "Amanda",
                "is-active": True,
                "language": "en",
                "last-name": "Gallagher",
                "meta": {},
                "modified-at": "2017-05-21T00:00:00Z",
                "phone": None,
                "username": "mark48",
                "zip": None,
            },
            "id": "f561aaf6-ef0b-f14d-4208-bb46a4ccb3ad",
            "relationships": {
                "acls": {"data": [], "meta": {"count": 0}},
                "created-by-user": {
                    "data": {
                        "id": "9336ebf2-5087-d91c-818e-e6e9ec29f8c1",
                        "type": "users",
                    }
                },
            },
            "type": "users",
        }
    },
    "status": 201,
}
