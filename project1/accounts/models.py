from django.db import models
from django.core.checks.messages import Error
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password, role='user'):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('User name is required')

        validate_password(password)

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        user.set_password(password)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='superadmin'
        )
        user.is_staff = user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    role_choices = [
        ('user', 'User'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
        ('superadmin', 'Superadmin'),
    ]
    role = models.CharField(
        max_length=20, choices=role_choices, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.role in ['superadmin', 'admin', 'staff']

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return self.first_name + " " + self.last_name
