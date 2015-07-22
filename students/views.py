from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import StudentForm, StudentLogForm, StudentLearningPlanForm, StudentGainPointsForm
from .models import Student, StudentLog, StudentGainPoints

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
    if pk:
        student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
             form.save()
             return HttpResponseRedirect(reverse('student_list'))
    else:
        form = StudentForm(instance=student)

    template_name = 'students/student_form.html'
    context = {'form': form}
    return render(request, template_name, context)


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return HttpResponseRedirect(reverse('student_list'))

    template_name = 'students/student_confirm_delete.html'
    context = {'object': student}
    return render(request, template_name, context)

def student_logcreate(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentLogForm(request.POST)
        if form.is_valid():
            f = StudentLog(student=student,
                           content=request.POST['content'],
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
    student = get_object_or_404(Student, pk=pk)
    learningplan = Student.objects.get(pk=pk)
    form = StudentLearningPlanForm(instance=student)

    if request.method == 'POST':
        form = StudentLearningPlanForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('student_list'))

    template_name = 'students/learningplan.html'
    context = {'learningplan': learningplan, 'form': form}
    return render(request, template_name, context)

def student_gainpoints(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentGainPointsForm(instance=student)
    if request.method == 'POST':
        form = StudentGainPointsForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['math_type'] != '' and form.cleaned_data['math_type'] != student.mathplan_type:
                print 'must be the same as the type in the Math Plan' #TODO - How to make this a Validation?
            if form.cleaned_data['reading_type'] != '' and form.cleaned_data['reading_type'] != student.readingplan_type:
                print 'must be the same as the type in the Reading Plan'
            f = StudentGainPoints(student=student,
                                  created_by = request.user,
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

            return HttpResponseRedirect(reverse('student_list'))
    template_name = 'students/student_gainpoints.html'
    context = {'student' : student, 'form': form}
    return render(request, template_name, context)

def student_gainpoints_list(request, pk):
    student = get_object_or_404(Student, pk=pk)
    object_list = StudentGainPoints.objects.filter(student_id=pk).order_by('-created_date')

    paginator = Paginator(object_list, 8, orphans=3)

    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(num_pages)

    template_name = 'students/student_gainpoints_list.html'
    context = {'object_list': object_list, 'student': student, }
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

def student_cru(request, search=None):
    print request.method

    if search:
        student = get_object_or_404(Student, pk=id)

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            print 'is valid'
            student = form.save(commit=False)
            student.added_how = 'individual add'
            student.added_how_detail = request.user
            student.save()
            return HttpResponseRedirect('/')
        else:
            print 'is not valid'
            context = {'form': StudentForm(data=request.POST)}
    else:
        form = StudentForm()
        context = {'form': form}

    template = 'students/student_form.html'
    return render(request, template, context)

