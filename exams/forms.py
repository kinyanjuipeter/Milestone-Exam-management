from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Course, Unit, Student, ExamRecord


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses."""
    class Meta:
        model = Course
        fields = ['name', 'school']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'school': forms.Select(attrs={'class': 'form-control'})
        }


class UnitForm(forms.ModelForm):
    """Form for creating and editing units."""
    class Meta:
        model = Unit
        fields = ['name', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit name'}),
            'course': forms.Select(attrs={'class': 'form-control'})
        }


class StudentForm(forms.ModelForm):
    """Form for creating and editing students."""
    class Meta:
        model = Student
        fields = ['name', 'registration_number', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student name'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration number'}),
            'course': forms.Select(attrs={'class': 'form-control'})
        }


class ExamRecordForm(forms.ModelForm):
    """Form for entering exam records."""
    class Meta:
        model = ExamRecord
        fields = ['student', 'unit', 'cat1_score', 'cat2_score', 'end_term_score']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'cat1_score': forms.NumberInput(attrs={
                'class': 'form-control cat-score',
                'placeholder': '0-30',
                'min': '0',
                'max': '30',
                'step': '0.01'
            }),
            'cat2_score': forms.NumberInput(attrs={
                'class': 'form-control cat-score',
                'placeholder': '0-30',
                'min': '0',
                'max': '30',
                'step': '0.01'
            }),
            'end_term_score': forms.NumberInput(attrs={
                'class': 'form-control end-term-score',
                'placeholder': '0-70',
                'min': '0',
                'max': '70',
                'step': '0.01'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter units based on the selected student's course
        if 'student' in self.fields:
            self.fields['student'].widget.attrs.update({'class': 'form-control'})
        if 'unit' in self.fields:
            self.fields['unit'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        cat1_score = cleaned_data.get('cat1_score')
        cat2_score = cleaned_data.get('cat2_score')
        end_term_score = cleaned_data.get('end_term_score')

        if cat1_score and (cat1_score < 0 or cat1_score > 30):
            raise forms.ValidationError("CAT 1 score must be between 0 and 30")

        if cat2_score and (cat2_score < 0 or cat2_score > 30):
            raise forms.ValidationError("CAT 2 score must be between 0 and 30")

        if end_term_score and (end_term_score < 0 or end_term_score > 70):
            raise forms.ValidationError("End-term score must be between 0 and 70")

        return cleaned_data


class StudentUnitForm(forms.Form):
    """Form for selecting student and unit for exam entry."""
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a student"
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a unit"
    ) 