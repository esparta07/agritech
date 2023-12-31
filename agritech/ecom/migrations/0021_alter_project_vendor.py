# Generated by Django 4.0.3 on 2023-05-17 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom', '0020_myimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='vendor',
            field=models.ForeignKey(limit_choices_to={'Q(role__exact=User.VENDOR) | Q(is_superadmin__exact=True)'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
