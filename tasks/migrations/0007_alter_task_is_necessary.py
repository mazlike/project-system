# Generated by Django 4.2.7 on 2024-12-20 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_is_necessary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='is_necessary',
            field=models.BooleanField(default=False, verbose_name='Необходимо'),
        ),
    ]
