# Generated by Django 4.2 on 2023-06-12 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0017_user_is_approved"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_approved",
        ),
    ]
