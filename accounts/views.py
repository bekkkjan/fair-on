# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import UserLoginForm, EmployerRegistrationForm, CandidateRegistrationForm
from .models import User


class UserLoginView(LoginView):
    """
    Foydalanuvchi kirish ko'rinishi
    """
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """
        Shakl tekshiruvdan o'tganda ishlaydi
        """
        # Foydalanuvchi tasdiqlangan yoki adminmi?
        user = form.get_user()
        if not user.is_verified and user.user_type == 'employer':
            messages.error(self.request, "Sizning hisobingiz hali admin tomonidan tasdiqlanmagan.")
            return self.form_invalid(form)

        # Foydalanuvchini tizimga kiritish
        login(self.request, user)
        messages.success(self.request, f"Xush kelibsiz, {user.full_name}!")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Muvaffaqiyatli kirishdan so'ng yo'naltiriladigan URL
        """
        if self.request.user.user_type == 'employer':
            return reverse_lazy('jobs:employer_dashboard')
        elif self.request.user.user_type == 'candidate':
            return reverse_lazy('jobs:candidate_dashboard')
        else:
            return reverse_lazy('core:home')


class EmployerRegistrationView(CreateView):
    """
    Ish beruvchi ro'yxatdan o'tish ko'rinishi
    """
    form_class = EmployerRegistrationForm
    template_name = 'accounts/employer_register.html'  # Make sure this matches the template name
    success_url = reverse_lazy('accounts:registration_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,
                         "Muvaffaqiyatli ro'yxatdan o'tildi! Admin tasdiqlagandan so'ng tizimga kirishingiz mumkin.")
        return response


class CandidateRegistrationView(CreateView):
    """
    Nomzod ro'yxatdan o'tish ko'rinishi
    """
    form_class = CandidateRegistrationForm
    template_name = 'accounts/candidate_register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        """
        Shakl tekshiruvdan o'tganda ishlaydi
        """
        response = super().form_valid(form)
        user = form.instance
        # Nomzodlar avtomatik tarzda tasdiqlanadi
        user.is_verified = True
        user.save()
        messages.success(self.request, "Muvaffaqiyatli ro'yxatdan o'tildi! Endi tizimga kirishingiz mumkin.")
        return response


class RegistrationSuccessView(TemplateView):
    """
    Ro'yxatdan o'tish muvaffaqiyatli yakunlangandan so'ng ko'rinish
    """
    template_name = 'accounts/registration_success.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Foydalanuvchi profili ko'rinishi
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.user_type == 'employer':
            profile = user.employer_profile
        elif user.user_type == 'candidate':
            profile = user.candidate_profile
        else:
            profile = None

        context['profile'] = profile
        return context


def user_logout(request):
    """
    Foydalanuvchi chiqish funksiyasi
    """
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqildi!")
    return redirect('core:home')