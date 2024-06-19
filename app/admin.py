from django.contrib import admin
from . import models


class CustomerAdmin(admin.ModelAdmin):
    model = models.Customer
    list_display = ("firstname", "othernames", "phonenumber_1", "email")
admin.site.register(models.Customer, CustomerAdmin)


class EmployerCompanyAdmin(admin.ModelAdmin):
    model = models.EmployerCompany
    list_display = ("name", "email", "address")
admin.site.register(models.EmployerCompany, EmployerCompanyAdmin)


class JobPositionAdmin(admin.ModelAdmin):
    model = models.JobPosition
    list_display = ("job_position", )
admin.site.register(models.JobPosition, JobPositionAdmin)


class JobAdmin(admin.ModelAdmin):
    model = models.Job
    list_display = ("job_title", "job_field", "job_position", "job_company_name")

    def job_company_name(self, obj):
        return obj.job_company.name
admin.site.register(models.Job, JobAdmin)


class RecruitmentProcessAdmin(admin.ModelAdmin):
    model = models.RecruitmentProcess
    list_display = ("customer_fullname","job_name", "company_name", "status")

    def customer_fullname(self, obj):
        firstname = obj.customer.firstname
        lastname = obj.customer.othernames
        return f"{firstname} {lastname}"
    
    def company_name(self, obj):
        return obj.job.job_company
    
    def job_name(self, obj):
        return obj.job.job_title
admin.site.register(models.RecruitmentProcess, RecruitmentProcessAdmin)


class FeesPaymentAdmin(admin.ModelAdmin):
    model = models.FeesPayment
    list_display = ("customer_fullname", "fee_type", "amount", "payment_status", "payment_date")

    def customer_fullname(self, obj):
        firstname = obj.customer.firstname
        lastname = obj.customer.othernames
        return f"{firstname} {lastname}"
admin.site.register(models.FeesPayment, FeesPaymentAdmin)


class ConnectionFeesAdmin(admin.ModelAdmin):
    model = models.ConnectionFees
    list_display = ("fees_amount", )
admin.site.register(models.ConnectionFees, ConnectionFeesAdmin)


class RegistrationFeesAdmin(admin.ModelAdmin):
    model = models.RegistrationFees
    list_display = ("fees_amount", )
admin.site.register(models.RegistrationFees, RegistrationFeesAdmin)


class ConsultationFeesAdmin(admin.ModelAdmin):
    model = models.ConsultationFees
    list_display = ("fees_amount", )
admin.site.register(models.ConsultationFees, ConsultationFeesAdmin)