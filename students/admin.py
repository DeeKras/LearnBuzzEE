from django.contrib import admin
from .models import Student, Parent, StudentLog, StudentGainPoints, StudentLearningPlanLog

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentLog)
admin.site.register(StudentGainPoints)
admin.site.register(StudentLearningPlanLog)

