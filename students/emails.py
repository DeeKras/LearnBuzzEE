from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

import requests
import easygui
from datetime import datetime

from .forms import EditEmailForm
from .models import Email
from .utils import strip_html, get_display, \
    MATHPLAN_CHOICES, READINGPLAN_CHOICES,\
    gender_he_she, gender_him_her

key = 'key-5b043e50a4c56d9ff6b8c73b5d23c3e4'
sandbox = 'sandboxa8420b597da7412d906e170e6e810830.mailgun.org'

request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)


def create_learned_email(request, student, f):
    guardian = 'dk' #will pull this from parent model
    signature = "your child's teacher" #will pull this from the teacher

    body = 'Hello {}:<br>'.format(guardian)
    body += "This is a progress report about {} {}. <br> I am so happy to share that ".format(
                    student.firstname, student.lastname)

    if f.math_amt != None:
        body += "in <b>MATH, {} has done {} {} from {} {}</b>".format(
                     gender_he_she(student.gender),
                     f.math_amt,
                     get_display(MATHPLAN_CHOICES, f.math_type),
                     f.math_source,
                     f.math_source_details)
    if f.math_amt != None and f.reading_amt != None:
        body += "<br> and "
    if f.reading_amt != None:
        body += "in <b>READING, {} has read {} {} from {} {}</b>".format(
                     gender_he_she(student.gender),
                     f.reading_amt,
                     get_display(READINGPLAN_CHOICES, f.reading_type),
                     f.reading_source,
                     f.reading_source_details)
    body += ". <br>Please encourage {} to keep it up! <br>". format(
                    gender_him_her(student.gender))
    body += signature

    email_from = 'LEARNBUZZY Mrs. K.<dee@deekras.com>' # will pull this from the teacher
    email_to = 'deekras2@gmail.com' #will pull this from parent model
    email_subject = 'Good news about {} {}'.format(student.firstname, student.lastname)
    email_html = "<html> {} </html>".format(body)

    user = student.user.id
    print user

    return create_email_log(request, user, email_from, email_to, email_subject, email_html)

def create_email_log(request, user, email_from, email_to, email_subject, email_html):
    email = Email(user=user,
                  email_from=email_from,
                  email_to=email_to,
                  email_subject=email_subject,
                  email_body=email_html,
                  created_by=request.user)
    email.save()
    return email.id


def email_no_send(email_id):
    email = Email.objects.get(id=email_id)

    email.status = "No Send"
    email.save()

    student_name = '{} {}'.format(email.student.firstname, email.student.lastname)
    easygui.msgbox("Email about {} was NOT sent".format(student_name), "Email")

    return HttpResponseRedirect(reverse('student_edit', args=(email.student.id,)))

def email_send(email_id):
    email = Email.objects.get(id=email_id)

    email_data = {'from': email.email_from,
            'to': email.email_to,
            'subject': email.email_subject,
            'html': email.email_body}

    request = requests.post(request_url,
        auth=('api', key),
        data=email_data)

    easygui.msgbox("Email was sent".format(student_name), "Email")

    email.status = 'sent'
    email.sent_date = datetime.now()
    email.save()

    return HttpResponseRedirect(reverse('student_edit', args=(email.student.id,)))

def email_preview(request,email_id):
    email = Email.objects.get(id=email_id)

    if request.POST['submit'] == 'no_send':
        email.save()
        return email_no_send(email_id)

    elif request.POST['submit'] == 'send':
        if request.POST['body_as_html']:
            email.email_body = request.POST['body_as_html']
        if request.POST['subject']:
            email.email_subject = request.POST['subject']
        if request.POST['to']:
            email.email_to = request.POST['to']
        email.save()

        return email_send(request,email_id)

    else: #preview
        body_no_html = strip_html(email.email_body)

        template_name = 'students/emails/email_preview.html'
        context = {'form': EditEmailForm(initial={
                                                'to': email.email_to,
                                                'subject': email.email_subject,
                                                'body_as_html': email.email_body,
                                                'body_no_html': body_no_html}),
                                                'from': email.email_from,
                                                'html': email.email_body,
                                                'email_id':email_id}

        return render(request, template_name, context)



