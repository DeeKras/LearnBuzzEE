from django import forms
from django.core.exceptions import ValidationError
from .models import Student,  StudentLog, StudentGainPoints, Group,\
            GENDER_CHOICES,  READINGPLAN_CHOICES, MATHPLAN_CHOICES


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student

        group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                       widget=forms.Select(attrs={'class':'selector'}))
        fields = ['firstname', 'lastname', 'gender',
                  'avatar', 'group',
                  'mathplan_points', 'mathplan_per', 'mathplan_type',
                  'readingplan_points','readingplan_per','readingplan_type']
        widgets = {
            'firstname': forms.TextInput(
                attrs={'placeholder':'First Name', 'class':'form-control'}),
            'lastname': forms.TextInput(
                attrs={'placeholder':'Last Name', 'class':'form-control'}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
            'mathplan_points':forms.Textarea(attrs={'cols':6, 'rows':1}),
            'mathplan_per':forms.Textarea(attrs={'cols': 6, 'rows': 1}),
            'mathplan_type': forms.Select(choices= MATHPLAN_CHOICES),
            'readingplan_points':forms.Textarea(attrs={'cols':6, 'rows':1}),
            'readingplan_per':forms.Textarea(attrs={'cols': 6, 'rows': 1}),
            'readingplan_type': forms.Select(choices= READINGPLAN_CHOICES)
        }

class StudentLogForm(forms.ModelForm):
    class Meta:
        model = StudentLog
        fields = ['content']


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

    def __init__(self,*args, **kwargs):
        self.student = kwargs.pop('student', None)
        super(StudentGainPointsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StudentGainPointsForm, self).clean()
        errorlist = {}
        print 'in clean'
        # print '{}? {}'.format(cleaned_data['math_type'], self.student.mathplan_type )
        if cleaned_data['math_type'] != self.student.mathplan_type:
                errorlist['math_type']='the math type must match the one in the Math Plan'
        elif cleaned_data['math_amt'] != None \
            or cleaned_data['math_type'] != '' \
            or cleaned_data['math_source'] != '':
                if cleaned_data['math_source'] == '':
                    errorlist['math_source']='must enter math source'
                if cleaned_data['math_amt'] == None:
                    errorlist['math_amt']='must enter math amt'
                if cleaned_data['math_type'] == '':
                    print cleaned_data['math_type']
                    errorlist['math_type']='must enter math type -------------'
        if cleaned_data['reading_amt'] != None \
            or cleaned_data['reading_type'] != '' \
            or cleaned_data['reading_source'] != '':
                if cleaned_data['reading_source'] == '':
                    errorlist['reading_source']='must enter reading source'
                if cleaned_data['reading_amt'] == None:
                    errorlist['reading_amt']='must enter reading amt'
                if cleaned_data['reading_type'] == '':
                    errorlist['reading_type']='must enter reading type'
        raise ValidationError(errorlist)

class EditEmailForm(forms.Form):
    to = forms.EmailField()
    subject = forms.CharField(max_length=100, widget= forms.Textarea(attrs={'cols': 140, 'rows': 1}))
    body_as_html = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 5}))
    body_no_html = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 5}))