# Generated by Django 5.0.6 on 2024-06-27 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_expenses'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expenses',
            new_name='Expense',
        ),
    ]