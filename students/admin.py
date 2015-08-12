from django.contrib import admin
from .models import Student, Guardian, StudentLog, StudentGainPoints, \
    StudentLearningPlanLog, Email,\
    StudentGroup,  UploadLog, Educator

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(StudentLog)
admin.site.register(StudentGainPoints)
admin.site.register(StudentLearningPlanLog)
admin.site.register(Email)
admin.site.register(StudentGroup)
admin.site.register(UploadLog)
admin.site.register(Educator)

