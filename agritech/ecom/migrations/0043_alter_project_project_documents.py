# Generated by Django 4.0.3 on 2023-07-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0042_project_project_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_documents',
            field=models.FileField(blank=True, null=True, upload_to='media/Project/documents/'),
        ),
    ]
