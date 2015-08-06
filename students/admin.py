from django.contrib import admin
from .models import Student, Parent, StudentLog, StudentGainPoints, \
    StudentLearningPlanLog, Email,\
    StudentGroup, Educator, UploadLog

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentLog)
admin.site.register(StudentGainPoints)
admin.site.register(StudentLearningPlanLog)
admin.site.register(Email)
admin.site.register(StudentGroup)
admin.site.register(Educator)
admin.site.register(UploadLog)

