from django.db.models import Q
from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User, Group


from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView



import re
from operator import attrgetter
from django.utils import timezone
from itertools import chain
import easygui
from copy import deepcopy
import csv


from .forms import StudentForm, StudentLogForm, StudentGainPointsForm, UploadFileForm
from .models import Student, StudentLog, StudentGainPoints, StudentLearningPlanLog,  UploadLog, Educator
from .emails import create_learned_email, email_preview, email_send, email_no_send
from .utils import get_display, MATHPLAN_CHOICES, READINGPLAN_CHOICES, GENDER_CHOICES


#----------------------------------------------
def student_retrieve(request):

    student_list = Student.objects.all().order_by('lastname', 'firstname')
    paginator = Paginator(student_list, 6, orphans=3)

    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(num_pages)

    context = {'students': students}
    template_name = 'students/student_list.html'
    return render(request, template_name, context)

def student_new_update(request, pk=None, student=None):
    if pk: #if is an edit
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)

        mode='edit'
    else:
        form = StudentForm()
        mode = 'new'

    #if it is an edit or new with data
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            if mode == 'new':
                # user = User.objects.create()
                student = form.save(commit=False)
                student.added_how = 'entered by {}'.format(request.user)

                user = User.objects._create_user(
                    username='{}{}'.format(student.firstname, student.lastname).replace(' ',''),
                    email=None,
                    password=student.firstname,
                    is_staff=False, is_superuser=False)
                group=Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()

                student.user = user
                student.save()
                add_LearningPlanLog(request, form, student, mode)
            elif mode == 'edit':
                old = get_object_or_404(Student, pk=pk)
                add_LearningPlanLog(request, form, student, mode, old )
                form.save()
            return HttpResponseRedirect(reverse('student_edit', args=(student.id,)))

    template_name = 'students/student_form.html'
    context = {'form': form, 'student': student, 'mode':mode}
    return render(request, template_name, context)


def educator_new_update(request, pk=None, educator=None):
    if pk: #if is an edit
        educator = get_object_or_404(Educator, pk=pk)
        form = StudentForm(instance=student)

        mode='edit'
    else:
        form = StudentForm()
        mode = 'new'

    #if it is an edit or new with data
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            if mode == 'new':
                # user = User.objects.create()
                student = form.save(commit=False)
                student.added_how = 'entered by {}'.format(request.user)

                user = User.objects._create_user(
                    username='{}{}'.format(student.firstname, student.lastname).replace(' ',''),
                    email=None,
                    password=student.firstname,
                    is_staff=False, is_superuser=False)
                group=Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()

                student.user = user
                student.save()
                add_LearningPlanLog(request, form, student, mode)
            elif mode == 'edit':
                old = get_object_or_404(Student, pk=pk)
                add_LearningPlanLog(request, form, student, mode, old )
                form.save()
            return HttpResponseRedirect(reverse('student_edit', args=(student.id,)))

    template_name = 'students/student_form.html'
    context = {'form': form, 'student': student, 'mode':mode}
    return render(request, template_name, context)

def add_LearningPlanLog(request, form,  student, mode, old= None):
    empty = (form.cleaned_data['mathplan_points'] == None and \
            form.cleaned_data['mathplan_per'] == None and  \
            form.cleaned_data['mathplan_type'] == '' and \
            form.cleaned_data['readingplan_points'] == None and \
            form.cleaned_data['readingplan_per'] == None and \
            form.cleaned_data['readingplan_type'] == '')

    changes = False
    if old != None:
        changes = (old.mathplan_points != form.cleaned_data['mathplan_points'] or \
               old.mathplan_per != form.cleaned_data['mathplan_per'] or \
               old.mathplan_type != form.cleaned_data['mathplan_type']or \
               old.readingplan_points != form.cleaned_data['readingplan_points'] or \
               old.readingplan_per != form.cleaned_data['readingplan_per'] or \
               old.readingplan_type != form.cleaned_data['readingplan_type'])

    if not empty:
        if mode == 'new' or changes:
           student.currentplan_id +=1
           student.save()
           g = StudentLearningPlanLog(student=student,
                                        created_by = request.user,
                                        plan_id = student.currentplan_id,
                                        mathplan_points = form.cleaned_data['mathplan_points'],
                                        mathplan_per = form.cleaned_data['mathplan_per'],
                                        mathplan_type = form.cleaned_data['mathplan_type'],
                                        readingplan_points = form.cleaned_data['readingplan_points'],
                                        readingplan_per = form.cleaned_data['readingplan_per'],
                                        readingplan_type = form.cleaned_data['readingplan_type'])

           g.save()


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_name = '{} {}'.format(student.firstname, student.lastname)
    if request.method == 'POST':
        if request.POST['submit'] == 'delete':
            student.delete()
            easygui.msgbox("{} was deleted".format(student_name), "Delete")
        else:
            easygui.msgbox("{} was not deleted".format(student_name), "Delete")

        return HttpResponseRedirect(reverse('student_list'))

    template_name = 'students/student_confirm_delete.html'
    context = {'object': student}
    return render(request, template_name, context)

def student_search(request):
    if request.GET['last']:
        s1 = Student.objects.filter(
            Q(lastname__istartswith=request.GET['last'])).order_by('lastname', 'firstname')
        for student in s1:
            student.result_type = "Startswith"

        s2= Student.objects.filter(
            ~Q(lastname__istartswith=request.GET['last'])&
            Q(lastname__icontains=request.GET['last'])).order_by('lastname', 'firstname')
        for student in s2:
            student.result_type = "Contains"

        results = chain(s1, s2)

        if len(s1) ==1 and len(s2) == 0:
            student = Student.objects.get(lastname__istartswith=request.GET['last'])
            form = StudentForm(instance=student)
            template_name = 'students/student_form.html'
            context = {'form': form, 'student': student}
        else:
            template_name = 'students/search_results_list.html'
            context = {'results': results,  'search': request.GET['last']}
        return render(request, template_name, context)

    else:
        return HttpResponseRedirect(reverse('student_list'))

def student_logcreate(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentLogForm(request.POST, instance=student)
        if form.is_valid():
            f = StudentLog(student=student,
                           content=form.cleaned_data['content'],
                           created_by=request.user)
            f.save()             # TODO: how to do this with form.save()?

            return HttpResponseRedirect(reverse('student_list'))
    else:
        form = StudentLogForm(instance=student)
        template_name = 'students/studentlog_form.html'
        context = {'form': form, 'student': student}
        return render(request, template_name, context)

def student_loglist(request, pk):
     student = get_object_or_404(Student, pk=pk)
     log_list = StudentLog.objects.filter(student_id=pk).order_by('-created_date')

     template_name = 'students/studentlog_list.html'
     context = {'log_list': log_list, 'student': student}
     return render(request, template_name, context)

def upload_file(request):
        error_text=''
        if request.method == 'POST':
            csvfile = request.FILES['file']

            if UploadLog.objects.filter(file_name=csvfile).exists():
                already_uploaded = UploadLog.objects.get(file_name=csvfile)
                students_in_uploaded_batch  = Student.objects.filter(added_how=already_uploaded.upload_id).order_by('lastname', 'firstname')
                error_text = '{} was uploaded on {: %b %d, %Y %I:%M%p} as Group {}'.format(csvfile, already_uploaded.uploaded_timestamp, already_uploaded.group)+"\n"+"with these students:"+"\n"
                for student in students_in_uploaded_batch:
                    error_text += '{}, {}'.format(student.lastname, student.firstname)+'\n'
                error_messages = {'already uploaded': error_text}

            else:
                #TODO - test to make sure it is a valid csv.
                #TODO - allow for valid csv or xls

                form = UploadFileForm(request.POST, request.FILES)

                if form.is_valid():
                    last_upload = UploadLog.objects.latest('upload_id')
                    new_upload = 'upload.'+str(int(last_upload.upload_id.split('.')[1])+1).zfill(4)

                    rows = csv.DictReader(csvfile,)
                    num_student_uploaded = 0
                    for row in rows:
                        user = User.objects._create_user(
                        username='{}{}'.format(row['firstname'], row['lastname']).replace(' ',''),
                        email=None,
                        password=row['firstname'],
                        is_staff=False, is_superuser=False)
                        group=Group.objects.get(name='Student')
                        user.groups.add(group)
                        user.save()

                        student = Student()
                        student.user = user
                        student.firstname = row['firstname']
                        student.lastname = row['lastname']
                        student.gender = row['gender']
                        student.group = form.cleaned_data['group']
                        student.added_how = new_upload
                        student.save()

                        num_student_uploaded +=1

                    add_to_log = UploadLog()
                    add_to_log.upload_id = new_upload
                    add_to_log.uploaded_by = request.user
                    add_to_log.file_name = csvfile
                    add_to_log.amt_uploaded = num_student_uploaded
                    add_to_log.group = form.cleaned_data['group']
                    add_to_log.save()
                    return HttpResponseRedirect(reverse('uploaded_list', args=(new_upload,)))

                print 'not valid'

        template_name = 'students/file_upload.html'
        context = {'form': UploadFileForm(), 'errors': error_text}
        return render(request, template_name, context)

def list_after_upload(request, upload_id):
    #TODO - save using serializer - http://www.django-rest-framework.org/api-guide/serializers/
    student_list = Student.objects.filter(added_how=upload_id).order_by('lastname', 'firstname')
    paginator = Paginator(student_list, 6, orphans=3)
    UploadedListFormset = modelformset_factory(
            Student,
            fields=('id', 'lastname', 'firstname',
                    'mathplan_points', 'mathplan_per', 'mathplan_type',
                    'readingplan_points','readingplan_per','readingplan_type'),
            widgets= {  'firstname': forms.TextInput(
                            attrs={'placeholder':'First Name', 'class':'form-control'}),
                        'lastname': forms.TextInput(
                            attrs={'placeholder':'Last Name', 'class':'form-control'}),
                        'mathplan_points':forms.TextInput(
                            attrs={'class': "input-numbers", 'placeholder': 'number'}),
                        'mathplan_per':forms.TextInput(
                            attrs={'class': "input-numbers", 'placeholder': 'number'}),
                        'mathplan_type': forms.Select(choices= MATHPLAN_CHOICES,
                            attrs={'class': "input-dropdown"}),
                        'readingplan_points':forms.TextInput(
                            attrs={'class': "input-numbers", 'placeholder': 'number'}),
                        'readingplan_per':forms.TextInput(
                            attrs={'class': "input-numbers", 'placeholder': 'number'}),
                        'readingplan_type': forms.Select(choices= READINGPLAN_CHOICES,
                            attrs={'class': "input-dropdown"})},
            extra=0)

    uploaded_formset = UploadedListFormset(queryset= student_list)

    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(num_pages)

    if request.POST:
        formset = UploadedListFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print formset.errors


    context = {'students': students, 'upload_id': upload_id, 'formset': uploaded_formset}
    template_name = 'students/uploaded_list.html'
    return render(request, template_name, context)


def student_gainpoints(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentGainPointsForm(instance=student)

    if request.method == 'POST':
        form = StudentGainPointsForm(request.POST, student=student)
        if form.is_valid():
        # create log of Gain Points
            f = StudentGainPoints(student=student,
                                  created_by = request.user,
                                  plan_id = student.currentplan_id,
                                  math_source = form.cleaned_data['math_source'],
                                  math_source_details = form.cleaned_data['math_source_details'],
                                  math_amt = form.cleaned_data['math_amt'],
                                  math_type = form.cleaned_data['math_type'],
                                  reading_source = form.cleaned_data['reading_source'],
                                  reading_source_details = form.cleaned_data['reading_source_details'],
                                  reading_amt = form.cleaned_data['reading_amt'],
                                  reading_type = form.cleaned_data['reading_type']
                                  )
            f.save() # TODO: how to do this with form.save()?

        # Add points to Student
            add_points(student, f.math_amt, f.reading_amt)
        # create the email data
            email_id = create_learned_email(request, student, f)
        #Email - Send, Don't Send, Preview
            if request.POST['submit'] == 'send':
                return email_send(request, email_id)
            elif request.POST['submit'] == 'no_send':
                return email_no_send(request, email_id)
            elif request.POST['submit'] == 'preview':
                return email_preview(request, email_id)

    template_name = 'students/student_gainpoints.html'
    context = {'student' : student, 'form': form}
    return render(request, template_name, context)

def add_points(student, math_amt=0, reading_amt=0):
      if math_amt != None:
        mathplan_points = student.mathplan_points
        mathplan_per = student.mathplan_per

        points_to_add = ((math_amt + student.math_remaining)/mathplan_per)*mathplan_points
        student.math_points += points_to_add
        student.total_points +=points_to_add
        remaining_to_add = ((math_amt + student.math_remaining)%mathplan_per)
        student.math_remaining = remaining_to_add

      if reading_amt != None:
        readingplan_points = student.readingplan_points
        readingplan_per = student.readingplan_per

        points_to_add = ((reading_amt + student.reading_remaining)/readingplan_per)*readingplan_points
        student.reading_points += points_to_add
        student.total_points +=points_to_add
        remaining_to_add = ((reading_amt + student.reading_remaining)%readingplan_per)
        student.reading_remaining = remaining_to_add
      student.save()

def student_gainpoints_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    learningplan_list = StudentLearningPlanLog.objects.filter(student=student).order_by('-created_date')
    points_list = StudentGainPoints.objects.filter(student=student).order_by('-created_date')

    object_list = StudentGainPoints.objects.filter(student_id=pk).order_by('-created_date')
    total = points_list.count

    # paginator = Paginator(object_list, 8, orphans=3)
    paginator = Paginator(points_list, 8, orphans=3)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(num_pages)

    template_name = 'students/student_gainpoints_list.html'
    context = {'object_list': object_list, 'student': student,
               'total': total, 'points_list': points_list, 'learningplan_list': learningplan_list}
    return render(request, template_name, context)


def student_spendpoints(request, pk):
    pass


class EducatorList(ListView):
    model = Educator
    paginate_by = 12

class EducatorCreate(CreateView):
    model = Educator

    fields = ['known_as', 'email_from', 'email_signature', 'group', ]
    success_url = reverse_lazy('student_list')

class EducatorEdit(UpdateView):
    model = Educator
    fields = ['known_as', 'email_from', 'email_signature', 'group',]
    success_url = reverse_lazy('student_list')

class EducatorDelete(DeleteView):
    model = Educator
    success_url = reverse_lazy('student_list')

#------------------------------------------------------

# def student_create(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.added_how = 'individual add'
#             student.added_how_detail = request.user
#             student.save()
#             return HttpResponseRedirect(reverse('student_list'))
#
#     template_name = 'students/student_form.html'
#     context = {'form': StudentForm()}
#     return render(request, template_name, context)
#
# def student_update(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method =='POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('student_list'))
#
#     template_name = 'students/student_form.html'
#     context = {'form': StudentForm(instance=student)}
#     return render(request, template_name, context)


#-------------------------------------------------------------






# def student_create(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.added_how = 'individual add'
#             student.added_how_detail = request.user
#             student.save()
#             return HttpResponseRedirect(reverse('student_list'))
#
#     template_name = 'students/student_form.html'
#     context = {'form': StudentForm()}
#     return render(request, template_name, context)
#
# def student_retrieve(request):
#     students = Student.objects.all()
#     context = {}
#
#     template_name = 'students/student_list.html'
#     context['object_list'] = students
#     return render(request, template_name, context)
#
# def student_update(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method =='POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('student_list'))
#
#     template_name = 'students/student_form.html'
#     context = {'form': StudentForm(instance=student)}
#     return render(request, template_name, context)
#
# def student_delete(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     if request.method == 'POST':
#         student.delete()
#         return HttpResponseRedirect(reverse('student_list'))
#
#     template_name = 'students/student_confirm_delete.html'
#     context = {'object': student}
#     return render(request, template_name, context)
#

#------------------------------------

# def student_cru(request, search=None):
#     print request.method
#
#     if search:
#         student = get_object_or_404(Student, pk=id)
#
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             print 'is valid'
#             student = form.save(commit=False)
#             student.added_how = 'individual add'
#             student.added_how_detail = request.user
#             student.save()
#             return HttpResponseRedirect('/')
#         else:
#             print 'is not valid'
#             context = {'form': StudentForm(data=request.POST)}
#     else:
#         form = StudentForm()
#         context = {'form': form}
#
#     template = 'students/student_form.html'
#     return render(request, template, context)

#search functionality from
# http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
# def normalize_query(query_string,
#                     findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
#                     normspace=re.compile(r'\s{2,}').sub):
#     ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
#         and grouping quoted words together.
#         Example:
#
#         >>> normalize_query('  some random  words "with   quotes  " and   spaces')
#         ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
#
#     '''
#     return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]
#
# def get_query(query_string, search_fields):
#     ''' Returns a query, that is a combination of Q objects. That combination
#         aims to search keywords within a model by testing the given search fields.
#
#     '''
#     query = None # Query to search for every search term
#     terms = normalize_query(query_string)
#     for term in terms:
#         or_query = None # Query to search for a given term in each field
#         for field_name in search_fields:
#             q = Q(**{"%s__icontains" % field_name: term})
#             if or_query is None:
#                 or_query = q
#             else:
#                 or_query = or_query | q
#         if query is None:
#             query = or_query
#         else:
#             query = query & or_query
#     return query
#
# def search(request, search_objects, search_fields, search_name='q'):
#     search_string = ''
#     results = search_objects
#     if (search_name in request.GET) and request.GET[search_name].strip():
#         search_string = request.GET[search_name]
#         object_query = get_query(search_string, search_fields)
#         results = search_objects.filter(object_query)
#     return results



#----------------------------------------------------
# class StudentList(ListView):
#     model = Student
#     paginate_by = 12
#
# class StudentCreate(CreateView):
#     model = Student
#     fields = ['firstname', 'lastname', 'gender',
#                   'avatar', 'group', ]
#     success_url = reverse_lazy('student_list')
#
# class StudentEdit(UpdateView):
#     model = Student
#     fields = ['firstname', 'lastname', 'gender',
#                   'avatar', 'group', ]
#     success_url = reverse_lazy('student_list')
#
# class StudentDelete(DeleteView):
#     model = Student
#     success_url = reverse_lazy('student_list')



