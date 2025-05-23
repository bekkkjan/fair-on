# Generated by Django 5.2 on 2025-05-02 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nomi')),
                ('description', models.TextField(blank=True, verbose_name='tavsif')),
            ],
            options={
                'verbose_name': 'vakansiya kategoriyasi',
                'verbose_name_plural': 'vakansiya kategoriyalari',
            },
        ),
        migrations.CreateModel(
            name='JobVacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='lavozim nomi')),
                ('requirements', models.TextField(verbose_name='talablar')),
                ('salary_min', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='minimal maosh')),
                ('salary_max', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='maksimal maosh')),
                ('location', models.CharField(max_length=255, verbose_name='joylashuv')),
                ('is_active', models.BooleanField(default=True, verbose_name='faol')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='yaratilgan sana')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobs.jobcategory')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='accounts.employerprofile')),
            ],
            options={
                'verbose_name': 'vakansiya',
                'verbose_name_plural': 'vakansiyalar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('applied', 'Ariza topshirilgan'), ('testing', "Testdan o'tish jarayonida"), ('completed', 'Testlar yakunlangan'), ('reviewed', "Ko'rib chiqilgan"), ('accepted', 'Qabul qilingan'), ('rejected', 'Rad etilgan')], default='applied', max_length=20, verbose_name='holat')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='ariza topshirilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='yangilangan sana')),
                ('diploma', models.FileField(blank=True, null=True, upload_to='applications/diplomas/', verbose_name='diplom nusxasi')),
                ('certificates', models.FileField(blank=True, null=True, upload_to='applications/certificates/', verbose_name='sertifikatlar')),
                ('work_history', models.FileField(blank=True, null=True, upload_to='applications/work_history/', verbose_name='mehnat daftarchasi')),
                ('personal_info', models.FileField(blank=True, null=True, upload_to='applications/personal_info/', verbose_name="nomzod haqida ma'lumotnoma")),
                ('professional_score', models.IntegerField(default=0, verbose_name='kasbiy test bali')),
                ('psychological_score', models.IntegerField(default=0, verbose_name='psixologik test bali')),
                ('corruption_score', models.IntegerField(default=0, verbose_name='korrupsiyaga moyillik bali')),
                ('total_score', models.IntegerField(default=0, verbose_name='umumiy ball')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.candidateprofile')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.jobvacancy')),
            ],
            options={
                'verbose_name': 'vakansiyaga nomzodlik',
                'verbose_name_plural': 'vakansiyaga nomzodliklar',
                'unique_together': {('vacancy', 'candidate')},
            },
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='savol matni')),
                ('question_type', models.CharField(choices=[('professional', "Kasbiy (soha bo'yicha)"), ('psychological', 'Psixologik'), ('corruption', 'Korrupsiyaga moyillik')], max_length=20, verbose_name='savol turi')),
                ('is_active', models.BooleanField(default=True, verbose_name='faol')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_questions', to='jobs.jobcategory')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_questions', to='accounts.employerprofile')),
            ],
            options={
                'verbose_name': 'test savoli',
                'verbose_name_plural': 'test savollari',
            },
        ),
        migrations.CreateModel(
            name='TestOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_text', models.CharField(max_length=255, verbose_name='variant matni')),
                ('points', models.IntegerField(default=0, verbose_name='ball')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='jobs.testquestion')),
            ],
        ),
        migrations.CreateModel(
            name='TestAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='javob berilgan sana')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_answers', to='jobs.jobapplication')),
                ('selected_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.testoption')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.testquestion')),
            ],
            options={
                'verbose_name': 'test javobi',
                'verbose_name_plural': 'test javoblari',
                'unique_together': {('application', 'question')},
            },
        ),
    ]
