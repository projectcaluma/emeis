# Generated by Django 3.2.25 on 2024-06-13 07:05

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


def set_all_parents(apps, schema_editor):
    from emeis.core.models import set_full_name_and_parents

    scope_model = apps.get_model("emeis_core.scope")
    for scope in scope_model.objects.all().iterator():
        # explicitly trigger the set_full_name signal handler
        set_full_name_and_parents(instance=scope, sender=set_all_parents)
        scope.save()


class Migration(migrations.Migration):
    dependencies = [
        ("emeis_core", "0011_mptt_to_tree_queries"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="scope",
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="scope",
            name="all_parents",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.UUIDField(), default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="scope",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="emeis_core.scope",
            ),
        ),
        migrations.AddIndex(
            model_name="scope",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["all_parents"], name="emeis_core__all_par_f8231c_gin"
            ),
        ),
        migrations.RunPython(set_all_parents, migrations.RunPython.noop),
    ]