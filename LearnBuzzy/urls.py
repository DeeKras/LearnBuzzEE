from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from students import views

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
    url(r'^points/gain/(?P<pk>\d+)$', 'students.views.student_gainpoints', name='student_gainpoints'),
    url(r'^points/spend/(?P<pk>\d+)$', 'students.views.student_spendpoints', name='student_spendpoints'),
    url(r'^points/list/(?P<pk>\d+)$', 'students.views.student_gainpoints_list', name='student_gainpoints_list'),
    url(r'^student/search/', 'students.views.student_search', name='student_search'),


    #emails
    # url(r'^email/preview/', 'students.emails.preview_email',name='preview_email'),
    url(r'^email/preview/(?P<email_id>\d+)$', 'students.emails.email_preview', name="email_preview"),
    # url(r'^', include('students.urls')),

    #upload files
    url(r'^upload$', 'students.views.upload_file', name="upload_file"),
    url(r'^upload/list/(?P<upload_id>[a-z]{6}\.\d{4})$', 'students.views.list_after_upload', name='uploaded_list'),

    #educator
    url(r'^educator/list$', views.EducatorList.as_view(), name='educator_list'),
    url(r'^educator/edit/(?P<id>\d+)$', views.EducatorEdit.as_view(), name='educator_edit'),
    url(r'^educator/new$', views.EducatorCreate.as_view(), name='educator_new'),
    url(r'^educator/delete/(?P<id>\d+)$', views.EducatorDelete.as_view(), name='educator_delete'),
]
urlpatterns += staticfiles_urlpatterns()