# Generated by Django 4.0.3 on 2023-06-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0038_project_is_soldout_alter_projectstatus_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='descrption_title',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.TextField(max_length=2000),
        ),
    ]
