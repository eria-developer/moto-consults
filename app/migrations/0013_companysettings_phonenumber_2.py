# Generated by Django 5.0.6 on 2024-07-30 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_employercompany_phone_number2'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysettings',
            name='phonenumber_2',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]