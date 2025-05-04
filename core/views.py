# core/views.py

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Count


# Comment these imports until migrations are applied successfully
# from jobs.models import JobVacancy, JobCategory

class HomeView(TemplateView):
    """
    Bosh sahifa ko'rinishi
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add empty lists for now to avoid the template error
        context['latest_vacancies'] = []
        context['categories'] = []

        # Once migrations are completed, uncomment this code:
        """
        # Eng so'nggi vakansiyalar
        try:
            from jobs.models import JobVacancy, JobCategory
            context['latest_vacancies'] = JobVacancy.objects.filter(is_active=True).order_by('-created_at')[:5]

            # Kategoriyalar bo'yicha vakansiyalar soni
            categories = JobCategory.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')[:5]
            context['categories'] = categories
        except:
            # If models are not yet available or table doesn't exist
            context['latest_vacancies'] = []
            context['categories'] = []
        """

        return context


class AboutView(TemplateView):
    """
    Loyiha haqida sahifa
    """
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """
    Aloqa sahifasi
    """
    template_name = 'core/contact.html'


class FaqView(TemplateView):
    """
    Ko'p beriladigan savollar sahifasi
    """
    template_name = 'core/faq.html'