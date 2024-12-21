# Generated by Django 4.2.7 on 2024-12-19 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_teacherapplication'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='repository', to='projects.project')),
            ],
        ),
    ]
