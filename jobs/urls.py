# jobs/urls.py

from django.urls import path
from . import views
from jobs.views import TakeTestView
app_name = 'jobs'

urlpatterns = [
    # Ish beruvchi uchun URL yo'llari
    path('employer/dashboard/', views.EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('employer/vacancies/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('employer/vacancies/create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('employer/vacancies/<int:pk>/update/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('employer/vacancies/<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('employer/test-questions/', views.TestQuestionListView.as_view(), name='test_question_list'),
    path('employer/test-questions/create/', views.TestQuestionCreateView.as_view(), name='test_question_create'),
    path('employer/applications/', views.ApplicationListView.as_view(), name='all_applications'),
    path('employer/vacancies/<int:vacancy_id>/applications/', views.ApplicationListView.as_view(),
         name='vacancy_applications'),
    path('employer/applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='employer_application_detail'),
    path('employer/vacancies/<int:vacancy_id>/rating/', views.ApplicationRatingView.as_view(),
         name='application_rating'),

    # Nomzod uchun URL yo'llari
    path('candidate/dashboard/', views.CandidateDashboardView.as_view(), name='candidate_dashboard'),
    path('vacancies/', views.CandidateVacancyListView.as_view(), name='vacancy_list_public'),
    path('vacancies/<int:pk>/', views.CandidateVacancyDetailView.as_view(), name='candidate_vacancy_detail'),
    path('vacancies/<int:vacancy_id>/apply/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/', views.CandidateApplicationDetailView.as_view(), name='application_detail'),
    path(
        "applications/<int:application_id>/test/<str:test_type>/",
        views.TakeTestView.as_view(),
        name="take_test"
    ),

    # Admin uchun URL yo'llari
    path('admin/employers/', views.EmployerVerificationListView.as_view(), name='employer_verification_list'),
    path('admin/employers/<int:user_id>/verify/', views.verify_employer, name='verify_employer'),
    path('admin/test-questions/', views.TestQuestionAdminListView.as_view(), name='admin_test_question_list'),
    path('admin/test-questions/create/', views.TestQuestionAdminCreateView.as_view(),
         name='admin_test_question_create'),
]