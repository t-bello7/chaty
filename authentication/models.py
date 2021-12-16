from django.db import models
from django.conf import settings
from django.contrib.auth.validators import (
    PermissionsMixin, UserManager, AbstractBaseUser

)
from django.contrib.auth.hashers import make_password
from helpers.models import TrackingModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class MyUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        """
            Create and save user with email and Password
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setderfault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True'))
        return  self._create_user(email, password, **extra_fields)

    
class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    """
    An abstract base classs implementing a fully featured User Model with admin-compliant permissions.

    """
    full_name = models.CharField(max_length=200)
    email = models.EmailField(_('email_address'), blank=True, unique=True)
    admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text= _(
            'Designates whether the user can log into this admin site.'
        )
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether the user can log application'
        ))
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            'Designates whether this users email is verified.'
        )
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
