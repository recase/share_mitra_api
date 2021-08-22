from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(gettext_lazy(
                'Superuser should have is_superuser field set to true.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(gettext_lazy(
                'Superuser should have is staff field set to true.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(gettext_lazy(
                'Superuser shoulf have is_active field set to true.'))

        return self.create_user(email, password, first_name,
                                last_name, **extra_fields)

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError(gettext_lazy('Email is required'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user
