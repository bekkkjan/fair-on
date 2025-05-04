# jobs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
import random
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages

from accounts.models import User
from .models import JobVacancy, TestQuestion, TestOption, JobApplication, TestAnswer
from .forms import JobVacancyForm, TestQuestionForm, TestOptionFormSet, JobApplicationForm, TestAnswerForm


# Ish beruvchi uchun ko'rinishlar






class EmployerRequiredMixin:
    """
    Faqat ish beruvchilar uchun ruxsat beruvchi mixin
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'employer' or not request.user.is_verified:
            messages.error(request, "Bu sahifaga kirishga ruxsat yo'q!")
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class EmployerDashboardView(EmployerRequiredMixin, TemplateView):
    """
    Ish beruvchi dashboard ko'rinishi
    """
    template_name = 'jobs/employer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer = self.request.user.employer_profile

        # Ish beruvchining vakansiyalari
        context['vacancies'] = JobVacancy.objects.filter(employer=employer)

        # Statistika
        context['total_vacancies'] = context['vacancies'].count()
        context['total_applications'] = JobApplication.objects.filter(vacancy__employer=employer).count()
        context['recent_applications'] = JobApplication.objects.filter(
            vacancy__employer=employer
        ).order_by('-created_at')[:5]

        return context


class VacancyListView(EmployerRequiredMixin, ListView):
    """
    Ish beruvchi vakansiyalari ro'yxati
    """
    model = JobVacancy
    template_name = 'jobs/employer/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return JobVacancy.objects.filter(employer=self.request.user.employer_profile)


class VacancyCreateView(EmployerRequiredMixin, CreateView):
    """
    Vakansiya yaratish
    """
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'jobs/employer/vacancy_form.html'
    success_url = reverse_lazy('jobs:vacancy_list')

    def form_valid(self, form):
        form.instance.employer = self.request.user.employer_profile
        messages.success(self.request, "Vakansiya muvaffaqiyatli yaratildi!")
        return super().form_valid(form)


class VacancyUpdateView(EmployerRequiredMixin, UpdateView):
    """
    Vakansiyani tahrirlash
    """
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'jobs/employer/vacancy_form.html'
    success_url = reverse_lazy('jobs:vacancy_list')

    def get_queryset(self):
        return JobVacancy.objects.filter(employer=self.request.user.employer_profile)

    def form_valid(self, form):
        messages.success(self.request, "Vakansiya muvaffaqiyatli yangilandi!")
        return super().form_valid(form)


class VacancyDeleteView(EmployerRequiredMixin, DeleteView):
    """
    Vakansiyani o'chirish
    """
    model = JobVacancy
    template_name = 'jobs/employer/vacancy_confirm_delete.html'
    success_url = reverse_lazy('jobs:vacancy_list')

    def get_queryset(self):
        return JobVacancy.objects.filter(employer=self.request.user.employer_profile)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Vakansiya muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)


class TestQuestionCreateView(EmployerRequiredMixin, CreateView):
    """
    Test savoli yaratish
    """
    model = TestQuestion
    form_class = TestQuestionForm
    template_name = 'jobs/employer/test_question_form.html'
    success_url = reverse_lazy('jobs:test_question_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['options_formset'] = TestOptionFormSet(self.request.POST)
        else:
            context['options_formset'] = TestOptionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        options_formset = context['options_formset']

        if options_formset.is_valid():
            form.instance.created_by = self.request.user.employer_profile
            self.object = form.save()
            options_formset.instance = self.object
            options_formset.save()
            messages.success(self.request, "Test savoli muvaffaqiyatli yaratildi!")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TestQuestionListView(EmployerRequiredMixin, ListView):
    """
    Test savollari ro'yxati
    """
    model = TestQuestion
    template_name = 'jobs/employer/test_question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return TestQuestion.objects.filter(
            Q(created_by=self.request.user.employer_profile) |
            Q(created_by__isnull=True)  # Tizim tomonidan yaratilgan savollar
        )


class ApplicationListView(EmployerRequiredMixin, ListView):
    """
    Vakansiyalarga tushgan arizalar ro'yxati
    """
    model = JobApplication
    template_name = 'jobs/employer/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        vacancy_id = self.kwargs.get('vacancy_id')
        if vacancy_id:
            return JobApplication.objects.filter(
                vacancy_id=vacancy_id,
                vacancy__employer=self.request.user.employer_profile
            )
        return JobApplication.objects.filter(
            vacancy__employer=self.request.user.employer_profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_id = self.kwargs.get('vacancy_id')
        if vacancy_id:
            context['vacancy'] = get_object_or_404(JobVacancy, id=vacancy_id)
        return context


class ApplicationDetailView(EmployerRequiredMixin, DetailView):
    """
    Ariza tafsilotlari
    """
    model = JobApplication
    template_name = 'jobs/employer/application_detail.html'
    # template_name = 'jobs/employer/application_rating.html'
    context_object_name = 'application'

    def get_queryset(self):
        return JobApplication.objects.filter(
            vacancy__employer=self.request.user.employer_profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = self.get_object()

        # Test javoblari
        context['test_answers'] = TestAnswer.objects.filter(application=application)

        return context


class ApplicationRatingView(EmployerRequiredMixin, TemplateView):
    """
    Nomzodlar reytingi
    """
    template_name = 'jobs/employer/application_rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_id = self.kwargs.get('vacancy_id')
        vacancy = get_object_or_404(JobVacancy, id=vacancy_id, employer=self.request.user.employer_profile)
        context['vacancy'] = vacancy

        # Eng yuqori balli nomzodlar (testlar to'liq topshirilgan)
        top_applications = JobApplication.objects.filter(
            vacancy=vacancy,
            status='completed'  # Faqat testlar yakunlangan nomzodlar
        ).order_by('-total_score')

        context['top_applications'] = top_applications[:10]  # Eng yaxshi 10 ta

        return context


# Nomzod uchun ko'rinishlar

class CandidateRequiredMixin:
    """
    Faqat nomzodlar uchun ruxsat beruvchi mixin
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'candidate':
            messages.error(request, "Bu sahifaga kirishga ruxsat yo'q!")
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class CandidateDashboardView(CandidateRequiredMixin, TemplateView):
    """
    Nomzod dashboard ko'rinishi
    """
    template_name = 'jobs/candidate/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidate = self.request.user.candidate_profile

        # Nomzodning arizalari
        context['applications'] = JobApplication.objects.filter(candidate=candidate)

        # Statistika
        context['total_applications'] = context['applications'].count()
        context['active_applications'] = context['applications'].exclude(
            status__in=['rejected', 'accepted']
        ).count()

        return context


class CandidateVacancyListView(ListView):
    """
    Barcha vakansiyalar ro'yxati
    """
    model = JobVacancy
    template_name = 'jobs/candidate/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return JobVacancy.objects.filter(is_active=True)


class CandidateVacancyDetailView(DetailView):
    """
    Vakansiya tafsilotlari
    """
    model = JobVacancy
    template_name = 'jobs/candidate/vacancy_detail.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Nomzod kirgan bo'lsa, ariza topshirgan yoki yo'qligini tekshirish
        if self.request.user.is_authenticated and self.request.user.user_type == 'candidate':
            candidate = self.request.user.candidate_profile
            vacancy = self.get_object()
            application = JobApplication.objects.filter(vacancy=vacancy, candidate=candidate).first()
            context['has_applied'] = application is not None
            context['application'] = application
        else:
            context['has_applied'] = False
        return context


@method_decorator(login_required, name='dispatch')
class ApplicationCreateView(CandidateRequiredMixin, CreateView):
    """
    Vakansiyaga ariza topshirish
    """
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/candidate/application_form.html'

    def get_success_url(self):
        return reverse('jobs:application_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_id = self.kwargs.get('vacancy_id')
        context['vacancy'] = get_object_or_404(JobVacancy, id=vacancy_id)
        return context

    def form_valid(self, form):
        vacancy_id = self.kwargs.get('vacancy_id')
        vacancy = get_object_or_404(JobVacancy, id=vacancy_id)
        candidate = self.request.user.candidate_profile

        # Tekshirish - bu vakansiyaga allaqachon ariza topshirilganmi
        existing_application = JobApplication.objects.filter(vacancy=vacancy, candidate=candidate).first()
        if existing_application:
            messages.error(self.request, "Siz bu vakansiyaga allaqachon ariza topshirgansiz!")
            return redirect('jobs:candidate_vacancy_detail', pk=vacancy.id)

        # Arizani saqlash
        form.instance.vacancy = vacancy
        form.instance.candidate = candidate
        form.instance.status = 'applied'

        messages.success(self.request, "Ariza muvaffaqiyatli topshirildi! Endi testlarni topshirishingiz kerak.")
        return super().form_valid(form)


class CandidateApplicationDetailView(CandidateRequiredMixin, DetailView):
    """
    Nomzodning arizasi tafsilotlari
    """
    model = JobApplication
    template_name = 'jobs/candidate/application_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        return JobApplication.objects.filter(candidate=self.request.user.candidate_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = self.get_object()

        # Testlarni topshirganmi?
        context['has_completed_tests'] = application.status in ['completed', 'reviewed', 'accepted', 'rejected']

        # Test natijalari
        if context['has_completed_tests']:
            context['test_results'] = {
                'professional': application.professional_score,
                'psychological': application.psychological_score,
                'corruption': application.corruption_score,
                'total': application.total_score
            }

        return context


class TakeTestView(CandidateRequiredMixin, TemplateView, LoginRequiredMixin, View):
    template_name = 'jobs/candidate/take_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application_id = self.kwargs.get('application_id')  # TO‘G‘RILANDI
        test_type = self.kwargs.get('test_type')

        application = get_object_or_404(
            JobApplication,
            id=application_id,
            candidate=self.request.user.candidate_profile
        )
        context['application'] = application
        context['test_type'] = test_type

        already_taken = False
        if test_type == 'professional' and application.professional_score > 0:
            already_taken = True
        elif test_type == 'psychological' and application.psychological_score > 0:
            already_taken = True
        elif test_type == 'corruption' and application.corruption_score > 0:
            already_taken = True

        context['already_taken'] = already_taken

        if not already_taken:
            if test_type == 'professional':
                questions = TestQuestion.objects.filter(
                    question_type='professional',
                    category=application.vacancy.category
                )[:30]
            elif test_type == 'psychological':
                questions = list(TestQuestion.objects.filter(question_type='psychological'))
                if len(questions) > 20:
                    questions = random.sample(questions, 20)
            elif test_type == 'corruption':
                questions = list(TestQuestion.objects.filter(question_type='corruption'))
                if len(questions) > 20:
                    questions = random.sample(questions, 20)
            else:
                questions = []

            if questions:
                context['question'] = questions[0]
                context['form'] = TestAnswerForm(question=questions[0])
                context['total_questions'] = len(questions)
                context['current_question'] = 1

                self.request.session[f'test_{test_type}_questions'] = [q.id for q in questions[1:]]
                self.request.session[f'test_{test_type}_answers'] = []
                self.request.session[f'test_{test_type}_current'] = 1
                self.request.session[f'test_{test_type}_total'] = len(questions)

        return context

    def post(self, request, application_id, test_type):
        application = get_object_or_404(JobApplication, id=application_id, candidate=request.user.candidate_profile)
        question_id = request.POST.get("question_id")
        selected_option_id = request.POST.get("selected_option")

        if not question_id or not selected_option_id:
            messages.error(request, "Iltimos, savolni va javobni tanlang.")
            return redirect(request.path)

        question = get_object_or_404(TestQuestion, id=question_id)
        selected_option = get_object_or_404(TestOption, id=selected_option_id)

        # Savolga javob saqlash
        if not TestAnswer.objects.filter(application=application, question=question).exists():
            TestAnswer.objects.create(
                application=application,
                question=question,
                selected_option=selected_option,
            )

        # Qolgan savollar
        remaining = request.session.get(f'test_{test_type}_questions', [])
        current = request.session.get(f'test_{test_type}_current', 1)

        if remaining:
            next_question_id = remaining.pop(0)
            next_question = get_object_or_404(TestQuestion, id=next_question_id)

            # Sessionni yangilash
            request.session[f'test_{test_type}_questions'] = remaining
            request.session[f'test_{test_type}_current'] = current + 1

            # Keyingi savolni ko‘rsatish
            context = {
                "application": application,
                "test_type": test_type,
                "question": next_question,
                "form": TestAnswerForm(question=next_question),
                "total_questions": request.session.get(f'test_{test_type}_total', 0),
                "current_question": current + 1,
                "already_taken": False,
            }

            return render(request, "jobs/candidate/take_test.html", context)

        # Test yakunlangan bo‘lsa — tegishli ballni hisoblab saqlash
        total_points = TestAnswer.objects.filter(application=application, question__question_type=test_type) \
                           .aggregate(score=Sum('selected_option__points'))['score'] or 0

        if test_type == 'professional':
            application.professional_score = total_points
        elif test_type == 'psychological':
            application.psychological_score = total_points
        elif test_type == 'corruption':
            application.corruption_score = total_points

        # Agar barcha 3 test yakunlangan bo‘lsa, holatni "completed" qilish
        if all([
            application.professional_score is not None,
            application.psychological_score is not None,
            application.corruption_score is not None
        ]):
            application.total_score = (
                    (application.professional_score or 0) +
                    (application.psychological_score or 0) +
                    (application.corruption_score or 0)
            )
            application.status = "completed"

        application.save()
        messages.success(request, f"{test_type.title()} testi yakunlandi.")
        return redirect("jobs:application_detail", pk=application.id)


# Admin ko'rinishlari

class AdminRequiredMixin:
    """
    Faqat adminlar uchun ruxsat beruvchi mixin
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Bu sahifaga kirishga ruxsat yo'q!")
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class EmployerVerificationListView(AdminRequiredMixin, ListView):
    """
    Tasdiqlanmagan ish beruvchilar ro'yxati
    """
    template_name = 'jobs/admin/employer_verification_list.html'
    context_object_name = 'employers'

    def get_queryset(self):
        return User.objects.filter(user_type='employer', is_verified=False)


@login_required
def verify_employer(request, user_id):
    """
    Ish beruvchini tasdiqlash
    """
    if not request.user.is_staff:
        messages.error(request, "Bu amalni bajarishga ruxsat yo'q!")
        return redirect('core:home')

    employer = get_object_or_404(User, id=user_id, user_type='employer')
    employer.is_verified = True
    employer.save()

    messages.success(request, f"{employer.full_name} muvaffaqiyatli tasdiqlandi!")
    return redirect('jobs:employer_verification_list')


class TestQuestionAdminListView(AdminRequiredMixin, ListView):
    """
    Barcha test savollari ro'yxati (admin uchun)
    """
    model = TestQuestion
    template_name = 'jobs/admin/test_question_list.html'
    context_object_name = 'questions'


class TestQuestionAdminCreateView(AdminRequiredMixin, CreateView):
    """
    Admin tomonidan test savoli yaratish
    """
    model = TestQuestion
    form_class = TestQuestionForm
    template_name = 'jobs/admin/test_question_form.html'
    success_url = reverse_lazy('jobs:admin_test_question_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['options_formset'] = TestOptionFormSet(self.request.POST)
        else:
            context['options_formset'] = TestOptionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        options_formset = context['options_formset']

        if options_formset.is_valid():
            self.object = form.save()
            options_formset.instance = self.object
            options_formset.save()
            messages.success(self.request, "Test savoli muvaffaqiyatli yaratildi!")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))




