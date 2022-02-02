# Generated by Django 2.2.26 on 2022-01-31 12:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("emeis_core", "0005_manager_on_user_model"),
    ]

    operations = [
        migrations.RenameField(model_name="acl", old_name="meta", new_name="metainfo"),
        migrations.RenameField(
            model_name="permission", old_name="meta", new_name="metainfo"
        ),
        migrations.RenameField(model_name="role", old_name="meta", new_name="metainfo"),
        migrations.RenameField(
            model_name="scope", old_name="meta", new_name="metainfo"
        ),
        migrations.RenameField(model_name="user", old_name="meta", new_name="metainfo"),
        migrations.AlterField(
            model_name="acl",
            name="metainfo",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict, verbose_name="metainfo"
            ),
        ),
        migrations.AlterField(
            model_name="permission",
            name="metainfo",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict, verbose_name="metainfo"
            ),
        ),
        migrations.AlterField(
            model_name="role",
            name="metainfo",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict, verbose_name="metainfo"
            ),
        ),
        migrations.AlterField(
            model_name="scope",
            name="metainfo",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict, verbose_name="metainfo"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="metainfo",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict, verbose_name="metainfo"
            ),
        ),
    ]