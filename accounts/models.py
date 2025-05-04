# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom foydalanuvchi menejeri
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Oddiy foydalanuvchi yaratish
        """
        if not email:
            raise ValueError(_('Email manzili kiritilishi shart'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Superuser (admin) yaratish
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser is_staff=True bo\'lishi kerak'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser is_superuser=True bo\'lishi kerak'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Asosiy foydalanuvchi modeli
    """
    USER_TYPE_CHOICES = (
        ('employer', 'Ish beruvchi'),
        ('candidate', 'Nomzod'),
        ('admin', 'Administrator'),
    )

    username = None
    email = models.EmailField(_('email manzil'), unique=True)
    user_type = models.CharField(_('foydalanuvchi turi'), max_length=20, choices=USER_TYPE_CHOICES)
    is_verified = models.BooleanField(_('tasdiqlangan'), default=False, help_text=_('Admin tomonidan tasdiqlangan'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class EmployerProfile(models.Model):
    """
    Ish beruvchi profili
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(_('tashkilot nomi'), max_length=255)
    company_address = models.CharField(_('tashkilot manzili'), max_length=255)
    position = models.CharField(_('lavozimi'), max_length=100)

    def __str__(self):
        return self.company_name


class CandidateProfile(models.Model):
    """
    Nomzod profili
    """
    EDUCATION_CHOICES = (
        ('higher', 'Oliy'),
        ('secondary_higher', 'Tayanch oliy'),
        ('secondary_special', 'O\'rta maxsus'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    patronymic = models.CharField(_('otasining ismi'), max_length=100)
    education = models.CharField(_('ma\'lumoti'), max_length=50, choices=EDUCATION_CHOICES)
    specialization = models.CharField(_('mutaxassisligi'), max_length=255)
    residential_address = models.CharField(_('doimiy yashash manzili'), max_length=255)
    passport_number = models.CharField(_('pasport raqami'), max_length=20)
    passport_pdf = models.FileField(_('pasport pdf nusxasi'), upload_to='passports/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.specialization}"