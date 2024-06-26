from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        # Ensure a role is provided or set a default role
        if 'role' not in extra_fields or extra_fields['role'] is None:
            default_role = Roles.objects.get_or_create(name='user')[0]
            extra_fields['role'] = default_role

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Set the role for superusers to 'admin'
        default_admin_role = Roles.objects.get_or_create(name='admin')[0]
        extra_fields['role'] = default_admin_role

        return self.create_user(email, password, **extra_fields)

class Roles(models.Model):
    name = models.CharField(max_length=40, default="user")

    def __str__(self):
        return f"{self.name}"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=30)
    othernames = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'othernames']

    def __str__(self):
        return self.email
