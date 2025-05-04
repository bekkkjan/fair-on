# jobs/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import JobVacancy, TestQuestion, TestOption, JobApplication, TestAnswer


class JobVacancyForm(forms.ModelForm):
    """
    Vakansiya yaratish formasi
    """

    class Meta:
        model = JobVacancy
        fields = ['title', 'category', 'requirements', 'salary_min', 'salary_max', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TestQuestionForm(forms.ModelForm):
    """
    Test savoli yaratish formasi
    """

    class Meta:
        model = TestQuestion
        fields = ['question_text', 'question_type', 'category']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class TestOptionForm(forms.ModelForm):
    """
    Test varianti yaratish formasi
    """

    class Meta:
        model = TestOption
        fields = ['option_text', 'points']
        widgets = {
            'option_text': forms.TextInput(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Test savoli va variantlarni yaratish uchun formset
TestOptionFormSet = forms.inlineformset_factory(
    TestQuestion, TestOption,
    form=TestOptionForm,
    extra=4,  # 4 variant yaratish
    max_num=4,  # maksimal 4 variant
    min_num=2,  # minimum 2 variant
    validate_min=True,
)


class JobApplicationForm(forms.ModelForm):
    """
    Vakansiyaga hujjat topshirish formasi
    """

    class Meta:
        model = JobApplication
        fields = ['diploma', 'certificates', 'work_history', 'personal_info']
        widgets = {
            'diploma': forms.FileInput(attrs={'class': 'form-control'}),
            'certificates': forms.FileInput(attrs={'class': 'form-control'}),
            'work_history': forms.FileInput(attrs={'class': 'form-control'}),
            'personal_info': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TestAnswerForm(forms.Form):
    """
    Test savoli javobini tanlash formasi
    """

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

        # Savolni ko'rsatish
        self.fields['question_text'] = forms.CharField(
            label=_('Savol'),
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'value': question.question_text
            })
        )

        # Javob variantlarini radio buttonlar sifatida ko'rsatish
        choices = [(option.id, option.option_text) for option in question.options.all()]
        self.fields['selected_option'] = forms.ChoiceField(
            label=_('Javobingizni tanlang'),
            choices=choices,
            widget=forms.RadioSelect()
        )

        # Savol ID sini hidden field sifatida saqlash
        self.fields['question_id'] = forms.IntegerField(
            widget=forms.HiddenInput(),
            initial=question.id
        )