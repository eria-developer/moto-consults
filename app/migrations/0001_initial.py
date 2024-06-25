# Generated by Django 5.0.6 on 2024-06-25 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=64)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicons/')),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectionFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('othernames', models.CharField(max_length=100, null=True)),
                ('phonenumber_1', models.CharField(max_length=15)),
                ('phonenumber_2', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(max_length=64)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='passport_photos/')),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='uploaded_files/')),
                ('remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployerCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=15)),
                ('description', models.TextField(null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_position', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_fee', models.IntegerField()),
                ('consultation_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='FeesPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_type', models.CharField(choices=[('registration', 'Registration Fee'), ('consultation', 'Consultation Fee'), ('connection', 'Connection Fee')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid'), ('partially_paid', 'Partially Paid')], default='unpaid', max_length=20)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=64)),
                ('job_field', models.CharField(blank=True, max_length=64, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('job_position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.jobposition')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('pending', 'Pending'), ('interviewed', 'Interviewed'), ('not_hired', 'Not Hired'), ('hired', 'Hired'), ('rejected_offer', 'Rejected the Offer')], default='applied', max_length=64)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('expected_salary', models.IntegerField(default=0)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.employercompany')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.job')),
            ],
        ),
    ]
