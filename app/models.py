from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class Customer(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False)
    othernames = models.CharField(max_length=100, null=True, blank=False)
    phonenumber_1 = models.CharField(max_length=15, null=False, blank=False)
    phonenumber_2 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=64, null=False, blank=False)
    # passport_photo = models.ImageField(upload_to="passport_photos/", null=False, blank=False)
    # file_upload = models.FileField(upload_to="uploaded_files/", null=False, blank=False)
    passport_photo = models.ImageField(upload_to="passport_photos/", null=True, blank=True)
    file_upload = models.FileField(upload_to="uploaded_files/", null=True, blank=True)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.firstname.title()} {self.othernames.title()} from {self.address}"
    

class EmployerCompany(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=64, null=False, blank=False)
    address = models.CharField(max_length=64, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.name} found in {self.address}"
    

class JobPosition(models.Model):
    job_position = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.job_position}"


class Job(models.Model):
    job_title = models.CharField(max_length=64, null=False, blank=False)
    job_position = models.ForeignKey(JobPosition, null=True, on_delete=models.CASCADE)
    job_field = models.CharField(max_length=64, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    job_company = models.ForeignKey(EmployerCompany, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.job_company:
            return f"{self.job_title} at {self.job_company}"
        return f"{self.job_title}"


class CompanySettings(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=64, null=False, blank=False)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    favicon = models.ImageField(upload_to="favicons/", null=True, blank=True)
    address = models.CharField(max_length=64, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class ConnectionFees(models.Model):
    fees_amount = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return f"{self.fees_amount}"


class RecruitmentProcess(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ("pending", "Pending"),
        ('interviewed', 'Interviewed'),
        ('not_hired', 'Not Hired'),
        ('hired', 'Hired'),
        ('rejected_offer', 'Rejected the Offer'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='applied')
    application_date = models.DateTimeField(auto_now_add=True)
    expected_salary = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.customer} - {self.job} - {self.status}"
    

class FeesPayment(models.Model):
    CUSTOMER_FEE_CHOICES = [
        ('registration', 'Registration Fee'),
        ('consultation', 'Consultation Fee'),
        ('connection', 'Connection Fee'),
    ]
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=20, choices=CUSTOMER_FEE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.firstname}'s {self.fee_type} payment"
    

class RegistrationFees(models.Model):
    fees_amount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"({self.fees_amount})"
    

class ConsultationFees(models.Model):
    fees_amount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.fees_amount}"
    
