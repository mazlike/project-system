# Generated by Django 4.2.7 on 2024-12-12 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='project',
        ),
        migrations.AddField(
            model_name='application',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='led_applications', to=settings.AUTH_USER_MODEL, verbose_name='Лидер команды'),
        ),
        migrations.AddField(
            model_name='application',
            name='project_description',
            field=models.TextField(null=True, verbose_name='Описание проекта'),
        ),
        migrations.AddField(
            model_name='application',
            name='project_title',
            field=models.CharField(max_length=255, null=True, verbose_name='Название проекта'),
        ),
        migrations.AddField(
            model_name='application',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervised_applications', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель проекта'),
        ),
        migrations.AddField(
            model_name='application',
            name='team_members',
            field=models.ManyToManyField(blank=True, related_name='applications_as_member', to=settings.AUTH_USER_MODEL, verbose_name='Участники команды'),
        ),
        migrations.AlterField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='application',
            name='applied_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL, verbose_name='Создан у'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default='Описание проекта отсутствует', verbose_name='Описание проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='led_projects', to=settings.AUTH_USER_MODEL, verbose_name='Лидер проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='Участники проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название проекта'),
        ),
        migrations.DeleteModel(
            name='Repository',
        ),
    ]
