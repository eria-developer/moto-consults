# Generated by Django 5.0.6 on 2024-06-19 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_recruitmentprocess_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruitmentprocess',
            name='company',
        ),
    ]
