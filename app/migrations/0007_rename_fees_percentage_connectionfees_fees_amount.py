# Generated by Django 5.0.6 on 2024-06-27 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_fees_amount_connectionfees_fees_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectionfees',
            old_name='fees_percentage',
            new_name='fees_amount',
        ),
    ]
