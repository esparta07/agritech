# Generated by Django 4.0.3 on 2023-07-11 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0047_project_address_project_city_project_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='address',
        ),
        migrations.RemoveField(
            model_name='project',
            name='city',
        ),
        migrations.RemoveField(
            model_name='project',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='project',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='project',
            name='state',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tole_no',
        ),
    ]
