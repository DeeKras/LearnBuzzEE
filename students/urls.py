from django.conf.urls import  url, patterns
from students.views import StudentList, StudentCreate, StudentEdit, StudentDelete

urlpatterns =  patterns('students.views',
    url(r'^$', StudentList.as_view(), name='student_list'),
    url(r'^new$', StudentCreate.as_view(), name ='student_new'),
    url(r'^edit/(?P<pk>\d+)$', StudentEdit.as_view(), name="student_edit"),
    url(r'^delete/(?P<pk>\d+)$', StudentDelete.as_view(), name='student_delete'),
    # url(r'^add_log/(?P<pk>\d+$', StudentLogCreate.as_view(), name='student_log_add'),
)
