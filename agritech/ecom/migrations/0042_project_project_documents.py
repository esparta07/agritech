# Generated by Django 4.0.3 on 2023-07-06 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0041_merge_20230629_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_documents',
            field=models.FileField(blank=True, null=True, upload_to='media/farmimages/documents/'),
        ),
    ]
