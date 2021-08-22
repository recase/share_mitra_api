from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'admin'
    SUBSCRIBED_USER = 'subscribed_user'
    USER = 'user'
    ROLES = (
        (ADMIN, 'admin'),
        (SUBSCRIBED_USER, 'subscribed user'),
        (USER, 'user'),
    )
    email = models.EmailField(gettext_lazy('Email address'), unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices=ROLES, default=USER, max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'
