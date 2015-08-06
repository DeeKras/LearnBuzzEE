from django import forms
from django.core.exceptions import ValidationError
from .models import Student,  StudentLog, StudentGainPoints, StudentGroup,\
            GENDER_CHOICES,  READINGPLAN_CHOICES, MATHPLAN_CHOICES


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student

        group = forms.ModelChoiceField(queryset=StudentGroup.objects.all(),
                                       widget=forms.Select(attrs={'class': "input-dropdown"}))
        fields = ['firstname', 'lastname', 'gender', 'id',
                  'avatar', 'group',
                  'mathplan_points', 'mathplan_per', 'mathplan_type',
                  'readingplan_points','readingplan_per','readingplan_type']
        widgets = {
            'id':forms.IntegerField(),
            'firstname': forms.TextInput(
                attrs={'placeholder':'First Name', 'class':'form-control'}),
            'lastname': forms.TextInput(
                attrs={'placeholder':'Last Name', 'class':'form-control'}),
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
            'mathplan_points':forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
            'mathplan_per':forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
            'mathplan_type': forms.Select(choices= MATHPLAN_CHOICES,
                                          attrs={'class': "input-dropdown"}),
            'readingplan_points':forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
            'readingplan_per':forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
            'readingplan_type': forms.Select(choices= READINGPLAN_CHOICES,
                                             attrs={'class': "input-dropdown"})
        }

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        errorlist = {}

        msg = "you must enter: "
        if cleaned_data['mathplan_points'] != None \
            or cleaned_data['mathplan_per'] != None \
            or cleaned_data['mathplan_type'] != '':
                if cleaned_data['mathplan_points'] == None:
                    errorlist['mathplan_points']= msg + 'number of points'
                if cleaned_data['mathplan_per'] == None:
                    errorlist['mathplan_per']= msg +'number of units'
                if cleaned_data['mathplan_type'] == '':
                    errorlist['mathplan_type']= msg + 'type of unit'
        if cleaned_data['readingplan_points'] != None \
            or cleaned_data['readingplan_per'] != None \
            or cleaned_data['readingplan_type'] != '':
                if cleaned_data['readingplan_points'] == None:
                    errorlist['readingplan_points']= msg + 'number of points'
                if cleaned_data['readingplan_per'] == None:
                    errorlist['readingplan_per']= msg +'number of units'
                if cleaned_data['readingplan_type'] == '':
                    errorlist['readingplan_type']= msg + 'type of unit'
        raise ValidationError(errorlist)

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
                'math_amt': forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
                'math_source': forms.TextInput(attrs={'class': "input-text"}),
                'math_source_details': forms.TextInput(attrs={'class': "input-text"}),
                'math_type': forms.Select(choices= MATHPLAN_CHOICES,
                                          attrs={'class': "input-dropdown"}),
                'reading_amt': forms.TextInput(attrs={'class': "input-numbers", 'placeholder': 'number'}),
                'reading_source': forms.TextInput(attrs={'class': "input-text"}),
                'reading_source_details': forms.TextInput   (attrs={'class': "input-text"}),
                'reading_type': forms.Select(choices=READINGPLAN_CHOICES,
                                             attrs={'class': "input-dropdown"})
        }

    def __init__(self,*args, **kwargs):
        self.student = kwargs.pop('student', None)
        super(StudentGainPointsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StudentGainPointsForm, self).clean()
        errorlist = {}

        msg = "you must enter: "

        if cleaned_data['math_type'] != '' and cleaned_data['math_type'] != self.student.mathplan_type:
                errorlist['math_type']='the math type must match the one in the Math Plan'
        elif cleaned_data['math_amt'] != None \
            or cleaned_data['math_type'] != '' \
            or cleaned_data['math_source'] != '':
                if cleaned_data['math_source'] == '':
                    errorlist['math_source']= msg + 'math source'
                if cleaned_data['math_amt'] == None:
                    errorlist['math_amt']= msg + 'math amt'
                if cleaned_data['math_type'] == '':
                    errorlist['math_type']= msg + 'math type'

        if cleaned_data['reading_type'] and cleaned_data['reading_type'] != self.student.readingplan_type:
                errorlist['reading_type']='the reading type must match the one in the Reading Plan'
        elif cleaned_data['reading_amt'] != None \
            or cleaned_data['reading_type'] != '' \
            or cleaned_data['reading_source'] != '':
                if cleaned_data['reading_source'] == '':
                    errorlist['reading_source']= msg + 'reading source'
                if cleaned_data['reading_amt'] == None:
                    errorlist['reading_amt']= msg + 'reading amt'
                if cleaned_data['reading_type'] == '':
                    errorlist['reading_type']= msg + 'reading type'
        raise ValidationError(errorlist)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Choose excel to upload")
    group = forms.ModelChoiceField(queryset=StudentGroup.objects.all(),
                                       widget=forms.Select(attrs={'class': "input-dropdown"}))


class EditEmailForm(forms.Form):
    to = forms.EmailField()
    subject = forms.CharField(max_length=100, widget= forms.Textarea(attrs={'cols': 140, 'rows': 1}))
    body_as_html = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 5}))
    body_no_html = forms.CharField(widget=forms.Textarea(attrs={'cols': 150, 'rows': 5}))

