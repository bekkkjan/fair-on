# jobs/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, EmployerProfile, CandidateProfile


class JobCategory(models.Model):
    name = models.CharField(_('nomi'), max_length=100)
    description = models.TextField(_('tavsif'), blank=True)

    class Meta:
        verbose_name = _('vakansiya kategoriyasi')
        verbose_name_plural = _('vakansiya kategoriyalari')

    def __str__(self):
        return self.name


class JobVacancy(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(_('lavozim nomi'), max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='vacancies')
    requirements = models.TextField(_('talablar'))
    salary_min = models.DecimalField(_('minimal maosh'), max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(_('maksimal maosh'), max_digits=10, decimal_places=2)
    location = models.CharField(_('joylashuv'), max_length=255)
    is_active = models.BooleanField(_('faol'), default=True)
    created_at = models.DateTimeField(_('yaratilgan sana'), auto_now_add=True)

    class Meta:
        verbose_name = _('vakansiya')
        verbose_name_plural = _('vakansiyalar')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.employer.company_name}"


class TestQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('professional', 'Kasbiy (soha bo\'yicha)'),
        ('psychological', 'Psixologik'),
        ('corruption', 'Korrupsiyaga moyillik'),
    )

    question_text = models.TextField(_('savol matni'))
    question_type = models.CharField(_('savol turi'), max_length=20, choices=QUESTION_TYPE_CHOICES)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='test_questions', null=True, blank=True)
    created_by = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='created_questions', null=True, blank=True)
    is_active = models.BooleanField(_('faol'), default=True)

    class Meta:
        verbose_name = _('test savoli')
        verbose_name_plural = _('test savollari')

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.question_text[:50]}."


class TestOption(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(_('variant matni'), max_length=255)
    points = models.IntegerField(_('ball'), default=0)

    def __str__(self):
        return self.option_text


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Ariza topshirilgan'),
        ('testing', 'Testdan o\'tish jarayonida'),
        ('completed', 'Testlar yakunlangan'),
        ('reviewed', 'Ko\'rib chiqilgan'),
        ('accepted', 'Qabul qilingan'),
        ('rejected', 'Rad etilgan'),
    )

    vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(_('holat'), max_length=20, choices=STATUS_CHOICES, default='applied')
    created_at = models.DateTimeField(_('ariza topshirilgan sana'), auto_now_add=True)
    updated_at = models.DateTimeField(_('yangilangan sana'), auto_now=True)

    diploma = models.FileField(_('diplom nusxasi'), upload_to='applications/diplomas/', null=True, blank=True)
    certificates = models.FileField(_('sertifikatlar'), upload_to='applications/certificates/', null=True, blank=True)
    work_history = models.FileField(_('mehnat daftarchasi'), upload_to='applications/work_history/', null=True, blank=True)
    personal_info = models.FileField(_('nomzod haqida ma\'lumotnoma'), upload_to='applications/personal_info/', null=True, blank=True)

    professional_score = models.IntegerField(_('kasbiy test bali'), default=0)
    psychological_score = models.IntegerField(_('psixologik test bali'), default=0)
    corruption_score = models.IntegerField(_('korrupsiyaga moyillik bali'), default=0)
    total_score = models.IntegerField(_('umumiy ball'), default=0)

    class Meta:
        verbose_name = _('vakansiyaga nomzodlik')
        verbose_name_plural = _('vakansiyaga nomzodliklar')
        unique_together = ['vacancy', 'candidate']

    def __str__(self):
        return f"{self.candidate.user.full_name} - {self.vacancy.title}"

    def update_total_score(self):
        self.total_score = self.professional_score + self.psychological_score + self.corruption_score
        self.save()


class TestAnswer(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='test_answers')
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(TestOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('javob berilgan sana'), auto_now_add=True)

    class Meta:
        verbose_name = _('test javobi')
        verbose_name_plural = _('test javoblari')
        unique_together = ['application', 'question']

    def __str__(self):
        return f"{self.application.candidate.user.full_name}: {self.question.question_text[:30]} - {self.selected_option.option_text}"
