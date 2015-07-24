from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import re
from operator import attrgetter
from django.utils import timezone
from itertools import chain


from .forms import StudentForm, StudentLogForm, StudentGainPointsForm
from .models import Student, StudentLog, StudentGainPoints, StudentLearningPlanLog





#----------------------------------------------
def student_retrieve(request):

    student_list = Student.objects.all().order_by('firstname').order_by('lastname')
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
    mode='new'

    if pk:
        student = get_object_or_404(Student, pk=pk)
        mode='edit'

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            if request.POST['submit'] == "Submit Student Information":
                form.save()
            if request.POST['submit'] == "Submit Learning Plan":
                f = form.save(commit=False)
                f.currentplan_id +=1
                f.save()
                g = StudentLearningPlanLog(student=student,
                                       created_by = request.user,
                                       plan_id = f.currentplan_id,
                                       mathplan_points = form.cleaned_data['mathplan_points'],
                                       mathplan_per = form.cleaned_data['mathplan_per'],
                                       mathplan_type = form.cleaned_data['mathplan_type'],
                                       readingplan_points = form.cleaned_data['readingplan_points'],
                                       readingplan_per = form.cleaned_data['readingplan_per'],
                                       readingplan_type = form.cleaned_data['readingplan_type'])

                g.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = StudentForm(instance=student)




    template_name = 'students/student_form.html'
    context = {'form': form, 'student': student, 'mode':mode}
    return render(request, template_name, context)


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
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


        print dir(results)

        if len(s1) == 1:
            student = Student.objects.get(lastname__istartswith=request.GET['last'])
            form = StudentForm(instance=student)
            template_name = 'students/student_form.html'
            context = {'form': form, 'student': student}
            return render(request, template_name, context)
        else:
            template_name = 'students/search_results_list.html'
            context = {'results': results, 'search': request.GET['last']}
            return render(request, template_name, context)

    else:
        return HttpResponseRedirect('/')


def student_logcreate(request, pk):
    print 'log create'
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

def student_learningplan(request, pk):
    print 'learning plan'
    student = get_object_or_404(Student, pk=pk)
    learningplan = Student.objects.get(pk=pk)
    form = StudentLearningPlanForm(instance=student)
    if request.method == 'POST':
        form = StudentLearningPlanForm(request.POST, instance=student)
        if form.is_valid():
            form.save()

            f = StudentLearningPlanLog(student=student,
                                       created_by = request.user,
                                       mathplan_points = cleaned_data['mathplan_points'],
                                       mathplan_per = cleaned_data['mathplan_per'],
                                       mathplan_type = cleaned_data['mathplan_type'],
                                       readingplan_points = cleaned_data['readingplan_points'],
                                       readingplan_per = cleaned_data['readingplan_per'],
                                       readingplan_type = cleaned_data['readingplan_type'])
            print f
            f.save()
            return HttpResponseRedirect(reverse('student_edit'))

    template_name = 'students/learningplan.html'
    context = {'learningplan': learningplan, 'form': form}
    return render(request, template_name, context)

def student_gainpoints(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentGainPointsForm(instance=student)
    if request.method == 'POST':
        form = StudentGainPointsForm(request.POST, student=student)
        if form.is_valid():
            if form.cleaned_data['math_type'] != '' and form.cleaned_data['math_type'] != student.mathplan_type:
                print 'must be the same as the type in the Math Plan' #TODO - How to make this a Validation?
            if form.cleaned_data['reading_type'] != '' and form.cleaned_data['reading_type'] != student.readingplan_type:
                print 'must be the same as the type in the Reading Plan'
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

            #add the points
            mathplan_points = student.mathplan_points
            mathplan_per = student.mathplan_per
            mathplan_type = student.mathplan_type

            print 'points {} | remaining {}'.format(student.math_points, student.math_remaining)
            print 'math he did {}'.format(f.math_amt)
            print 'math plan {} points per {} {}'.format(student.mathplan_points, student.mathplan_per, student.mathplan_type)
            points_to_add = ((f.math_amt + student.math_remaining)/mathplan_per)*mathplan_points

            student.math_points += points_to_add
            student.total_points +=points_to_add
            remaining_to_add = ((f.math_amt + student.math_remaining)%mathplan_per)
            student.math_remaining = remaining_to_add
            student.save()
            print 'points {} | remaining {}'.format(student.math_points, student.math_remaining)


            return HttpResponseRedirect(reverse('student_list'))
    template_name = 'students/student_gainpoints.html'
    context = {'student' : student, 'form': form}
    return render(request, template_name, context)

def student_gainpoints_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    learningplan_list = StudentLearningPlanLog.objects.filter(student=student).order_by('-created_date')
    points_list = StudentGainPoints.objects.filter(student=student).order_by('-created_date')

    print student.lastname, student.firstname

    for i, plan in enumerate(learningplan_list):
        if i !=0:
            print '{}: {} points per {} {}'.\
                format(plan.created_date, plan.mathplan_points, plan.mathplan_per, plan.mathplan_type)
            firstdate= learningplan_list[i-1].created_date
        else:
            print 'Current Learning Plan: {} points per {} {}'.\
                format(plan.mathplan_points, plan.mathplan_per, plan.mathplan_type)
            firstdate= timezone.now()
        seconddate= learningplan_list[i].created_date

        for points in points_list:
            if seconddate < points.created_date <firstdate:
                print "--", points.created_date, points.math_amt, points.math_type, points.math_source

    # object_list = sorted(learningplan_list + points_list, key=attrgetter('created_date'), reverse=True)

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



