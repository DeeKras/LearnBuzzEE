from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

import requests
import easygui
from datetime import datetime

from .forms import EditEmailForm
from .models import Email
from .utils import strip_html

key = 'key-5b043e50a4c56d9ff6b8c73b5d23c3e4'
sandbox = 'sandboxa8420b597da7412d906e170e6e810830.mailgun.org'

request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)

def create_learned_email(request, student, email, caregiver, student_name, what_learned):
    body = 'Hello {}:<br>'.format(caregiver)
    body = body + \
            "This is to inform you that <b>{} has learned {}</b>. <br>Please encourage him to keep it up!".\
                format(student_name, what_learned)
    email_from = 'LEARNBUZZY Mrs. K.<dee@deekras.com>'
    email_to = email
    email_subject = 'Good news about {}'.format(student_name)
    email_html = "<html> {} </html>".format(body)

    return create_email_log(request, student, email_from, email_to, email_subject, email_html)

def create_email_log(request, student, email_from, email_to, email_subject, email_html):
    email = Email(student=student,
                  email_from=email_from,
                  email_to=email_to,
                  email_subject=email_subject,
                  email_body=email_html,
                  created_by=request.user)
    email.save()
    return email.id


def email_no_send(request, email_id):
    email = Email.objects.get(id=email_id)

    email.status = "No Send"
    email.save()

    student_name = '{} {}'.format(email.student.firstname, email.student.lastname)
    easygui.msgbox("Email about {} was NOT sent".format(student_name), "Email")

    return HttpResponseRedirect(reverse('student_list'))

def email_send(request, email_id):
    email = Email.objects.get(id=email_id)

    email_data = {'from': email.email_from,
            'to': email.email_to,
            'subject': email.email_subject,
            'html': email.email_body}

    request = requests.post(request_url,
        auth=('api', key),
        data=email_data)

    student_name = '{} {}'.format(email.student.firstname, email.student.lastname)
    easygui.msgbox("Email about {} was sent".format(student_name), "Email")

    email.status = 'sent'
    email.sent_date = datetime.now()
    email.save()

    print 'Status: {0}'.format(request.status_code)
    print 'Body:   {0}'.format(request.text)

    return HttpResponseRedirect(reverse('student_list'))

def email_preview(request, email_id):
    email = Email.objects.get(id=email_id)
    if request.POST['submit'] == 'no_send':
        return email_no_send(request, email_id)
    elif request.POST['submit'] == 'send':
        if request.POST['body_as_html']:
            email.email_body = request.POST['body_as_html']
        if request.POST['subject']:
            email.email_subject = request.POST['subject']
        if request.POST['to']:
            email.email_to = request.POST['to']
        email.save()

        return email_send(request,email_id)

    else:
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



