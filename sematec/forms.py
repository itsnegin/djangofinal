
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import (
    Course,
    Instructor,
    InstructorProfile,
    StudentProfile,
)


class NewCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'category', 'instructor', 'image',
            'description', 'rate', 'teacher', 'price',
            'duration', 'level', 'certificate',
            'prerequisites', 'capacity', 'start_date',
        ]
        labels = {
            'title': _('Course title'),
            'category': _('Category'),
            'instructor': _('Instructor'),
            'image': _('Course image'),
            'description': _('Description'),
            'rate': _('Rating'),
            'teacher': _('Teacher'),
            'price': _('Price'),
            'duration': _('Duration'),
            'level': _('Level'),
            'certificate': _('Certificate'),
            'prerequisites': _('Prerequisites'),
            'capacity': _('Capacity'),
            'start_date': _('Start date'),
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'certificate':
                field.widget.attrs['class'] = 'form-check-input'
            elif name in ('level', 'category', 'instructor'):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['category'].empty_label = _('Select a category')
        self.fields['instructor'].empty_label = _('Select an instructor')


class UserInfoForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'photo', 'phone', 'city', 'city_fa',
            'father_name', 'national_code', 'birth_date',
            'gender', 'education',
        ]
        labels = {
            'photo': _('Photo'),
            'phone': _('Phone number'),
            'city': _('City'),
            'city_fa': _('City in Persian'),
            'father_name': _("Father's name"),
            'national_code': _('National code'),
            'birth_date': _('Birth date'),
            'gender': _('Gender'),
            'education': _('Education'),
        }
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in ('gender', 'education'):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class TeacherForm(ModelForm):
    class Meta:
        model = Instructor
        fields = ['name', 'name_fa', 'bio', 'bio_fa', 'photo']
        labels = {
            'name': _('Name (English)'),
            'name_fa': _('Name (Persian)'),
            'bio': _('Biography (English)'),
            'bio_fa': _('Biography (Persian)'),
            'photo': _('Photo'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class InstructorProfileForm(ModelForm):
    class Meta:
        model = InstructorProfile
        fields = [
            'national_code', 'birth_date', 'gender',
            'education', 'city', 'city_fa', 'phone', 'email',
        ]
        labels = {
            'national_code': _('National code'),
            'birth_date': _('Birth date'),
            'gender': _('Gender'),
            'education': _('Education'),
            'city': _('City (English)'),
            'city_fa': _('City (Persian)'),
            'phone': _('Phone number'),
            'email': _('Email'),
        }
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in ('gender', 'education'):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class AddStudentForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control rounded'

    def clean_username(self):
        username = self.cleaned_data['username']

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username