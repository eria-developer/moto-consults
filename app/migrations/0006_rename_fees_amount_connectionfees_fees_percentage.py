# Generated by Django 5.0.6 on 2024-06-27 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_expense_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectionfees',
            old_name='fees_amount',
            new_name='fees_percentage',
        ),
    ]