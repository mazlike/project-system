# Generated by Django 4.2.7 on 2024-12-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_file_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='user_file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
