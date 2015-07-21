from django import forms
from .models import Student,  StudentLog, StudentGainPoints, \
            GENDER_CHOICES, GROUPS_LIST, READINGPLAN_CHOICES, MATHPLAN_CHOICES


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname', 'gender',
                  'avatar', 'group', ]
        widgets = {
            'firstname': forms.TextInput(
                attrs={'placeholder':'First Name', 'class':'form-control'}),
            'lastname': forms.TextInput(
                attrs={'placeholder':'First Name', 'class':'form-control'}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
            'group': forms.RadioSelect(choices=GROUPS_LIST)
        }

class StudentLogForm(forms.ModelForm):
    class Meta:
        model = StudentLog
        fields = ['content']


class StudentLearningPlanForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['mathplan_points', 'mathplan_per', 'mathplan_type',
                  'readingplan_points','readingplan_per','readingplan_type']
        widgets = {
                'mathplan_type': forms.RadioSelect(choices= MATHPLAN_CHOICES),
                'readingplan_type': forms.RadioSelect(choices= READINGPLAN_CHOICES)
        }

class StudentGainPointsForm(forms.ModelForm):
    class Meta:
        model = StudentGainPoints
        fields = ['math_source','math_source_details','math_amt','math_type',
                  'reading_source','reading_source_details','reading_amt','reading_type']
        widgets = {
                'math_source': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
                'math_source_details': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
                'math_type': forms.Select(choices= MATHPLAN_CHOICES),
                'reading_source': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
                'reading_source_details': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
                'reading_type': forms.Select(choices=READINGPLAN_CHOICES)
        }

