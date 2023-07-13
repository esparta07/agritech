# Generated by Django 4.0.3 on 2023-07-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0049_project_address_project_latitude_project_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]