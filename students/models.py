from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


GROUPS_LIST = (
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D')
        )

GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        )

MATHPLAN_CHOICES = (
        ('li', 'lines'),
        ('ex','examples'),
        )

READINGPLAN_CHOICES = (
        ('li', 'lines'),
        ('pg','pages'),
        ('ch', 'chapters'),
        ('bk','books'),
        )




class Student(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,
                             choices=GENDER_CHOICES,
                             blank=False)
    avatar = models.ImageField(upload_to='thumbpath', blank=True)
    group = models.CharField(max_length=1,
                             choices=GROUPS_LIST)

    start_date = models.DateField(auto_now_add=True)
    added_how = models.CharField(max_length=100)
    added_how_detail = models.CharField(max_length=255)

#TODO figure out how to make the remaning be a dictionary {'lines': 0,}
    total_points = models.PositiveIntegerField(default=0)
    math_points = models.IntegerField(default=0)
    math_remaining = models.IntegerField(default=0)
    reading_points = models.PositiveIntegerField(default=0)
    reading_remaining = models.IntegerField(default=0)

    mathplan_points = models.PositiveIntegerField(null=True, blank=True)
    mathplan_per = models.PositiveIntegerField(null=True, blank=True)
    mathplan_type = models.CharField(max_length=2,
                                     choices= MATHPLAN_CHOICES, blank=True)

    readingplan_points = models.PositiveIntegerField(null=True, blank=True)
    readingplan_per = models.PositiveIntegerField(null=True, blank=True)
    readingplan_type = models.CharField(max_length=2,
                                     choices= READINGPLAN_CHOICES, blank=True)

    class Meta:
        verbose_name_plural = 'students'

    def __unicode__(self):
        return u'{}, {}'.format(self.lastname, self.firstname)

class Parent(models.Model):
    student = models.ManyToManyField(Student)
    user = models.OneToOneField(User)

    class Meta:
        verbose_name_plural = 'parents'

    def __unicode__(self):
        return u'{} {}'.format(self.user.first_name, self.user.last_name)


class StudentLog(models.Model):
    student = models.ForeignKey(Student)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'student logs'

    def __unicode__(self):
        return u'{}, {} log on {}'.format(self.student.lastname, self.student.firstname, self.created_date)

class StudentGainPoints(models.Model):
    student = models.ForeignKey(Student)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)

    math_source = models.TextField(blank=True)
    math_source_details = models.TextField(blank=True)
    math_amt = models.PositiveIntegerField(blank=True, null=True)
    math_type = models.CharField(max_length=2,
                                     choices= MATHPLAN_CHOICES,
                                    blank=True)

    reading_source = models.TextField(blank=True)
    reading_source_details = models.TextField(blank=True)
    reading_amt = models.PositiveIntegerField(blank=True, null=True)
    reading_type = models.CharField(max_length=2,
                                     choices= READINGPLAN_CHOICES,
                                    blank=True)

    def clean(self):

            errorlist = {}
            if self.math_amt != None or self.math_type != '' or self.math_source != '':
                if self.math_source == '':
                    errorlist['math_source']='must enter math source'
                if self.math_amt == None:
                    errorlist['math_amt']='must enter math amt'
                if self.math_type == '':
                    errorlist['math_type']='must enter math type'
            if self.reading_amt != None or self.reading_type != '' or self.reading_source != '':
                if self.reading_source == '':
                    errorlist['reading_source']='must enter reading source'
                if self.reading_amt == None:
                    errorlist['reading_amt']='must enter reading amt'
                if self.reading_type == '':
                    errorlist['reading_type']='must enter reading type'


            raise ValidationError(errorlist)


    def __unicode__(self):
        return '{}, {} gained points on {}'.format(self.student.lastname, self.student.firstname, self.created_date)