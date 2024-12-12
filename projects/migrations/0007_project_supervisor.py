# Generated by Django 4.2.7 on 2024-12-12 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0006_remove_application_project_application_leader_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_projects', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель проекта'),
        ),
    ]
