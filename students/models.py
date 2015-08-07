from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.utils import timezone

from .utils import GENDER_CHOICES, MATHPLAN_CHOICES, READINGPLAN_CHOICES


class Educator(models.Model):
    user = models.OneToOneField(User)
    known_as = models.CharField(max_length=100)
    email_from = models.CharField(max_length=100)
    student_group = models.CharField(max_length=10)
    email_signature = models.TextField()

    start_date = models.DateField(auto_now_add=True)
    added_how = models.CharField(max_length=100)
    added_how_detail = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'educators'

    def __unicode__(self):
        return u'{}'.format(self.called)


class StudentGroup(models.Model):
    groupname = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'groups'

    def __unicode__(self):
        return u'{} '.format(self.groupname)




class Student(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=30, blank=False)
    lastname = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1,
                             choices=GENDER_CHOICES,
                             blank=False)
    group = models.ForeignKey(StudentGroup)
    avatar = models.ImageField(upload_to='thumbpath', blank=True)

    start_date = models.DateField(auto_now_add=True)
    added_how = models.CharField(max_length=100)
    added_how_detail = models.CharField(max_length=255)

#TODO figure out how to make the remaning be a dictionary {'lines': 0,}
    total_points = models.PositiveIntegerField(default=0)
    math_points = models.IntegerField(default=0)
    math_remaining = models.IntegerField(default=0)
    reading_points = models.PositiveIntegerField(default=0)
    reading_remaining = models.IntegerField(default=0)

#current plan
    currentplan_id = models.PositiveIntegerField(default=0)

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
        permissions = (
            ("view_student_avatar", "Can change the avatar"),)

    def __unicode__(self):
        return u'{}: {}, {}'.format(self.pk, self.lastname, self.firstname)

class Email(models.Model):
    student = models.ForeignKey(Student)
    email_from = models.CharField(max_length=250)
    email_to = models.EmailField()
    email_cc = models.EmailField(blank=True)
    email_subject = models.CharField(max_length=250)
    email_body = models.TextField()

    status = models.CharField(max_length=25, default='draft')

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    sent_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'emails'

    def __unicode__(self):
        return 'email: status {}. created on {}'.format(self.status, self.created_date)

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

class StudentLearningPlanLog(models.Model):
    student = models.ForeignKey(Student)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    plan_id = models.PositiveIntegerField(null=True, blank=True)

    mathplan_points = models.PositiveIntegerField(null=True, blank=True)
    mathplan_per = models.PositiveIntegerField(null=True, blank=True)
    mathplan_type = models.CharField(max_length=2, choices= MATHPLAN_CHOICES)

    readingplan_points = models.PositiveIntegerField(null=True, blank=True)
    readingplan_per = models.PositiveIntegerField(null=True, blank=True)
    readingplan_type = models.CharField(max_length=2, choices= READINGPLAN_CHOICES)

    class Meta:
        verbose_name_plural = 'StudentLearningPlanLogs'

    def __unicode__(self):
        return '{}, {} learning plan on {}'.format(self.student.lastname, self.student.firstname, self.created_date)

class StudentGainPoints(models.Model):
    student = models.ForeignKey(Student)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=30)
    plan_id = models.PositiveIntegerField()

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

    class Meta:
        verbose_name_plural = 'Student.GainPoints'

    def __unicode__(self):
        return '{}, {} gained points on {}'.format(self.student.lastname, self.student.firstname, self.created_date)

class UploadLog(models.Model):
    upload_id = models.CharField(max_length=15)
    uploaded_by = models.CharField(max_length=30)
    uploaded_timestamp = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=300)
    amt_uploaded = models.IntegerField()
    group = models.ForeignKey(StudentGroup)

    def __unicode__(self):
        return '{}: Group {} on {} by {}'.\
            format(self.upload_id, self.group.groupname, self.uploaded_timestamp, self.uploaded_by)