# Generated by Django 5.0.6 on 2024-06-19 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_files/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='passport_photos/'),
        ),
    ]
