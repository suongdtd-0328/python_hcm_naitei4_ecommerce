from django.db import models
from django.core.checks.messages import Error
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
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
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
    username = models.CharField(
        max_length=50, unique=True, verbose_name=_('username'))
    email = models.EmailField(
        max_length=100, unique=True, verbose_name=_('email address'))
    phone_number = models.CharField(
        max_length=50, verbose_name=_('phone number'))

    # required
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name=_('date joined'))
    last_login = models.DateTimeField(
        auto_now_add=True, verbose_name=_('last login'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))

    role_choices = [
        ('user', _('User')),
        ('staff', _('Staff')),
        ('admin', _('Admin')),
        ('superadmin', _('Superadmin')),
    ]
    role = models.CharField(
        max_length=20, choices=role_choices, default='user', verbose_name=_('role'))

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
