# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_user_export 1"] = [
    ["Name", "First Name", "Email", "Roles and organizations"],
    [
        "Marsh",
        "Heather",
        "dmiller@example.org",
        """Barbara Gomez: Cody West
Katherine Gardner: Kevin Wood""",
    ],
    ["Ortega", "Nicole", "vgarcia@example.com", "Michelle Harris: Andrea Cunningham"],
    ["Osborne", "Aaron", "tonymata@example.net", "Christopher Thornton: Brooke Hill"],
    ["Grimes", "Ricky", "david81@example.net", "Zachary Garrett: Andrew Ruiz"],
    ["Morales", "David", "scottvalencia@example.net", "Anne Perkins: Christine Cooper"],
    ["Chan", "Connor", "jacqueline41@example.com", "Robert Barnes: Erica Hawkins"],
    ["Short", "Julia", "vdyer@example.net", "Kevin Franco: Alexis Sanchez"],
    ["Brown", "Robert", "xchase@example.org", "Rebecca Mullins: John Hill"],
    ["Campbell", "Jeremy", "lucas09@example.net", "Alicia Wells: Tracy Wallace MD"],
    [
        "Obrien",
        "Melissa",
        "theresaanderson@example.com",
        "Kristina Davis: David Taylor",
    ],
]
