from django.core.files import File
from django.http import HttpResponseRedirect


GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        )

MATHPLAN_CHOICES = (
        ('', 'choose unit type'),
        ('li', 'lines'),
        ('ex','examples'),
        )

READINGPLAN_CHOICES = (
        ('', 'choose unit type'),
        ('li', 'lines'),
        ('pg','pages'),
        ('ch', 'chapters'),
        ('bk','books'),
        )


def get_display(choice_list, code):
        return next(extended for shortened, extended in choice_list if shortened==code)


def strip_html(html):
        import re, cgi
        tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
        no_tags = tag_re.sub('', html)
        ready_for_web = cgi.escape(no_tags)
        return ready_for_web

def gender_him_her(gender):
        return 'him' if gender == "M" else 'her'

def gender_he_she(gender):
        return 'he' if gender == "M" else 'she'

def upload_file(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                print 'do data check'
                return HttpResponseRedirect(reverse('student_list'))
            print 'not valid'

        template_name = 'students/file_upload.html'
        context = {'form': UploadFileForm()}
        return render(request, template_name, context)

