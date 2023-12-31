# Generated by Django 4.0.3 on 2023-07-19 09:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0050_alter_project_latitude_alter_project_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Notice', max_length=100, null=True)),
                ('notice', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('audience', models.CharField(choices=[('V', 'Vendor'), ('U', 'User'), ('B', 'Both')], default='B', max_length=1)),
            ],
        ),
    ]
