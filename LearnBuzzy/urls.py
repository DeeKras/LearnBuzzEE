from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

#home
    # url(r'^$', 'students.views.home', name='home'),

#students

    url(r'^$', 'students.views.student_retrieve', name='student_list'),
    url(r'^new$', 'students.views.student_new_update', name ='student_new'),
    url(r'^edit/(?P<pk>\d+)$', 'students.views.student_new_update', name='student_edit'),
    url(r'^delete/(?P<pk>\d+)$', 'students.views.student_delete', name='student_delete'),
    url(r'^log_create/(?P<pk>\d+)$', 'students.views.student_logcreate', name='student_log_add'),
    url(r'^log_list/(?P<pk>\d+)$', 'students.views.student_loglist', name='student_log_list'),
    url(r'^learningplan/(?P<pk>\d+)$', 'students.views.student_learningplan', name='student_learningplan'),
    url(r'^points/gain/(?P<pk>\d+)$', 'students.views.student_gainpoints', name='student_gainpoints'),
    url(r'^points/spend/(?P<pk>\d+)$', 'students.views.student_spendpoints', name='student_spendpoints'),
    # url(r'^', include('students.urls')),

    ]