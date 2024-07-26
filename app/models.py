from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from datetime import timedelta
from django.utils import timezone



class Customer(models.Model):
    firstname = models.CharField(max_length=254, null=False, blank=False)
    othernames = models.CharField(max_length=254, null=True, blank=False)
    phonenumber_1 = models.CharField(max_length=254, null=False, blank=False)
    phonenumber_2 = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=254, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    passport_photo = models.ImageField(upload_to="passport_photos/", null=True, blank=True)
    file_upload = models.FileField(upload_to="uploaded_files/", null=True, blank=True)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.firstname.title()} {self.othernames.title()} from {self.address}"
    
    def calculate_progress():
        now = timezone.now()
        total_customers = Customer.objects.count()

        # Customers added in the last 30 days
        current_period_customers = Customer.objects.filter(date_added__gte=now - timedelta(days=30)).count()

        # Customers added in the 30 days before the last 30 days
        previous_period_customers = Customer.objects.filter(date_added__gte=now - timedelta(days=60), date_added__lt=now - timedelta(days=30)).count()

        if previous_period_customers == 0:
            increase_percentage = 0 if current_period_customers == 0 else 100
        else:
            increase_percentage = ((current_period_customers - previous_period_customers) / previous_period_customers) * 100

        return current_period_customers, increase_percentage
    

class EmployerCompany(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    address = models.CharField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=254, null=False, blank=False)
    phone_number2 = models.CharField(max_length=254, null=True)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} found in {self.address}"
    
    def calculate_progress():
        now = timezone.now()
        total_companies = EmployerCompany.objects.count()

        # Companies added in the last 30 days
        current_period_companies = EmployerCompany.objects.filter(date_added__gte=now - timedelta(days=30)).count()

        # Companies added in the 30 days before the last 30 days
        previous_period_companies = EmployerCompany.objects.filter(date_added__gte=now - timedelta(days=60), date_added__lt=now - timedelta(days=30)).count()

        if previous_period_companies == 0:
            increase_percentage = 0 if current_period_companies == 0 else 100
        else:
            increase_percentage = ((current_period_companies - previous_period_companies) / previous_period_companies) * 100

        return current_period_companies, increase_percentage
    

class JobPosition(models.Model):
    job_position = models.CharField(max_length=254)
    date_added = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.job_position}"


class Job(models.Model):
    job_title = models.CharField(max_length=254, null=False, blank=False)
    job_position = models.ForeignKey(JobPosition, null=True, on_delete=models.CASCADE)
    job_field = models.CharField(max_length=254, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    # job_company = models.ForeignKey(EmployerCompany, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.job_position:
            return f"{self.job_position} {self.job_title}"
        return f"{self.job_title}"
    
    def calculate_progress():
        now = timezone.now()
        total_jobs = Job.objects.count()

        # Jobs added in the last 30 days
        current_period_jobs = Job.objects.filter(date_added__gte=now - timedelta(days=30)).count()

        # Jobs added in the 30 days before the last 30 days
        previous_period_jobs = Job.objects.filter(date_added__gte=now - timedelta(days=60), date_added__lt=now - timedelta(days=30)).count()

        if previous_period_jobs == 0:
            increase_percentage = 0 if current_period_jobs == 0 else 100
        else:
            increase_percentage = ((current_period_jobs - previous_period_jobs) / previous_period_jobs) * 100

        return current_period_jobs, increase_percentage
    


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
    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, null=True, blank=False)
    status = models.CharField(max_length=254, choices=STATUS_CHOICES, default='applied')
    application_date = models.DateTimeField(auto_now_add=True)
    expected_salary = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.customer.firstname} - {self.job} - {self.company.name}"
    
    def calculate_progress():
        now = timezone.now()
        total_placements = RecruitmentProcess.objects.count()

        # Placements added in the last 30 days
        current_period_placements = RecruitmentProcess.objects.filter(application_date__gte=now - timedelta(days=30)).count()

        # Placements added in the 30 days before the last 30 days
        previous_period_placements = RecruitmentProcess.objects.filter(application_date__gte=now - timedelta(days=60), application_date__lt=now - timedelta(days=30)).count()

        if previous_period_placements == 0:
            increase_percentage = 0 if current_period_placements == 0 else 100
        else:
            increase_percentage = ((current_period_placements - previous_period_placements) / previous_period_placements) * 100

        return current_period_placements, increase_percentage
    

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
    fee_type = models.CharField(max_length=254, choices=CUSTOMER_FEE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=254, choices=STATUS_CHOICES, default='unpaid')
    payment_date = models.DateTimeField(auto_now_add=True)
    # payment_date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer.firstname}'s {self.fee_type} payment made on {self.payment_date}"
    

class Consultation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    consultation_fee = models.IntegerField()
    consultation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} consulted on {self.consultation_date}"
    


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            self.__class__.objects.all().delete()  # Delete all existing instances
        super().save(*args, **kwargs)

class ConnectionFees(SingletonModel):
    fees_amount = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return f"{self.fees_amount}"

class RegistrationFees(SingletonModel):
    fees_amount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"({self.fees_amount})"

class ConsultationFees(SingletonModel):
    fees_amount = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.fees_amount}"


class CompanySettings(SingletonModel):
    name = models.CharField(max_length=254, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    favicon = models.ImageField(upload_to="favicons/", null=True, blank=True)
    address = models.CharField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=254, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"
    

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=254)
    category = models.CharField(max_length=254)
    amount = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"