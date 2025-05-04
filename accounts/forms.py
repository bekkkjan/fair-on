# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User, EmployerProfile, CandidateProfile


class UserLoginForm(AuthenticationForm):
    """
    Foydalanuvchi kirish formasi
    """
    username = forms.EmailField(
        label=_("Email manzil"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email kiriting'})
    )
    password = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kiriting'})
    )


# accounts/forms.py - EmployerRegistrationForm class updated

class EmployerRegistrationForm(UserCreationForm):
    """
    Ish beruvchi ro'yxatdan o'tish formasi
    """
    first_name = forms.CharField(
        label=_("Ism"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingizni kiriting'})
    )
    last_name = forms.CharField(
        label=_("Familiya"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangizni kiriting'})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingizni kiriting'})
    )
    password1 = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni kiriting'})
    )
    password2 = forms.CharField(
        label=_("Parolni tasdiqlash"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni qayta kiriting'})
    )
    company_name = forms.CharField(
        label=_("Tashkilot nomi"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tashkilot nomini kiriting'})
    )
    company_address = forms.CharField(
        label=_("Tashkilot manzili"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tashkilot manzilini kiriting'})
    )
    position = forms.CharField(
        label=_("Lavozimi"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lavoziminggizni kiriting'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # Asosiy foydalanuvchini saqlash
        user = super().save(commit=False)
        user.user_type = 'employer'
        user.username = None  # Make sure username is not required
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Ish beruvchi profilini saqlash
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_address=self.cleaned_data['company_address'],
                position=self.cleaned_data['position']
            )

        return user


class CandidateRegistrationForm(UserCreationForm):
    """
    Nomzod ro'yxatdan o'tish formasi
    """
    first_name = forms.CharField(
        label=_("Ism"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingizni kiriting'})
    )
    last_name = forms.CharField(
        label=_("Familiya"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangizni kiriting'})
    )
    patronymic = forms.CharField(
        label=_("Otasining ismi"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otangizning ismini kiriting'})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email manzilingizni kiriting'})
    )
    password1 = forms.CharField(
        label=_("Parol"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni kiriting'})
    )
    password2 = forms.CharField(
        label=_("Parolni tasdiqlash"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni qayta kiriting'})
    )
    education = forms.ChoiceField(
        label=_("Ma'lumoti"),
        choices=CandidateProfile.EDUCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialization = forms.CharField(
        label=_("Mutaxassisligi"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mutaxassisligingizni kiriting'})
    )
    residential_address = forms.CharField(
        label=_("Yashash manzili"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doimiy yashash manzilingizni kiriting'})
    )
    passport_number = forms.CharField(
        label=_("Pasport raqami"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pasport raqamingizni kiriting'})
    )
    passport_pdf = forms.FileField(
        label=_("Pasport nusxasi (PDF)"),
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,  # Dastlabki versiyada faylsiz ham ro'yxatdan o'tish mumkin
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # Asosiy foydalanuvchini saqlash
        user = super().save(commit=False)
        user.user_type = 'candidate'
        user.username = None  # Username kerak emas, email ishlatiladi
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Nomzod profilini saqlash
            CandidateProfile.objects.create(
                user=user,
                patronymic=self.cleaned_data['patronymic'],
                education=self.cleaned_data['education'],
                specialization=self.cleaned_data['specialization'],
                residential_address=self.cleaned_data['residential_address'],
                passport_number=self.cleaned_data['passport_number'],
                passport_pdf=self.cleaned_data.get('passport_pdf')
            )

        return user