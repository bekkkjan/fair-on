# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Kirish va chiqish
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Ro'yxatdan o'tish
    path('register/employer/', views.EmployerRegistrationView.as_view(), name='employer_register'),
    path('register/candidate/', views.CandidateRegistrationView.as_view(), name='candidate_register'),
    path('register/success/', views.RegistrationSuccessView.as_view(), name='registration_success'),

    # Profil
    path('profile/', views.ProfileView.as_view(), name='profile'),
]