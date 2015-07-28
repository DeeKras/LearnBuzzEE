from django.contrib import admin
from .models import Student, Parent, StudentLog, StudentGainPoints, \
    StudentLearningPlanLog, Email,\
    Group, Educator

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentLog)
admin.site.register(StudentGainPoints)
admin.site.register(StudentLearningPlanLog)
admin.site.register(Email)
admin.site.register(Group)
admin.site.register(Educator)

