# Generated by Django 4.2 on 2023-06-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0021_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="state",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
