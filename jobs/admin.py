# jobs/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    JobCategory,
    JobVacancy,
    TestQuestion,
    TestOption,
    JobApplication,
    TestAnswer
)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    """
    Vakansiya kategoriyalari admin konfiguratsiyasi
    """
    list_display = ('name', 'vacancy_count')
    search_fields = ('name',)

    def vacancy_count(self, obj):
        return obj.vacancies.count()

    vacancy_count.short_description = _('Vakansiyalar soni')


class TestOptionInline(admin.TabularInline):
    """
    Test savoli variantlarini test savoli sahifasida ko'rsatish
    """
    model = TestOption
    min_num = 2
    max_num = 4
    extra = 2


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    """
    Test savollari admin konfiguratsiyasi
    """
    list_display = ('get_short_question', 'question_type', 'category', 'created_by', 'is_active')
    list_filter = ('question_type', 'category', 'is_active')
    search_fields = ('question_text',)
    inlines = [TestOptionInline]

    def get_short_question(self, obj):
        return f"{obj.question_text[:50]}..." if len(obj.question_text) > 50 else obj.question_text

    get_short_question.short_description = _('Savol')


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    """
    Vakansiyalar admin konfiguratsiyasi
    """
    list_display = ('title', 'employer', 'category', 'salary_range', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'employer__company_name', 'requirements')
    date_hierarchy = 'created_at'

    def salary_range(self, obj):
        return f"{obj.salary_min} - {obj.salary_max}"

    salary_range.short_description = _('Maosh oralig\'i')


class TestAnswerInline(admin.TabularInline):
    """
    Test javoblarini ariza sahifasida ko'rsatish
    """
    model = TestAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'created_at')
    can_delete = False


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """
    Vakansiyaga nomzodliklar admin konfiguratsiyasi
    """
    list_display = (
    'candidate', 'vacancy', 'status', 'professional_score', 'psychological_score', 'corruption_score', 'total_score',
    'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('candidate__user__first_name', 'candidate__user__last_name', 'vacancy__title')
    readonly_fields = ('professional_score', 'psychological_score', 'corruption_score', 'total_score')
    date_hierarchy = 'created_at'
    inlines = [TestAnswerInline]


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    """
    Test javoblari admin konfiguratsiyasi
    """
    list_display = ('application', 'question', 'selected_option', 'created_at')
    list_filter = ('question__question_type', 'created_at')
    search_fields = (
    'application__candidate__user__first_name', 'application__candidate__user__last_name', 'question__question_text')
    date_hierarchy = 'created_at'