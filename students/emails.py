import requests
from django.shortcuts import render

from .forms import EditEmailForm
from .utils import strip_html

key = 'key-5b043e50a4c56d9ff6b8c73b5d23c3e4'
sandbox = 'sandboxa8420b597da7412d906e170e6e810830.mailgun.org'

request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)

def create_learned_email(email, caregiver, student_name, what_learned):
    body = 'Hello {}:<br>'.format(caregiver)
    body = body + \
            "This is to inform you that <b>{} has learned {}</b>. <br>Please encourage him to keep it up!".\
                format(student_name, what_learned)
    email_from = 'LEARNBUZZY Mrs. K.<dee@deekras.com>'
    email_to = email
    email_subject = 'Good news about {}'.format(student_name)
    email_html = "<html> {} </html>".format(body)
    return email_from, email_to, email_subject, email_html

def send_email(email_data):
    email_from, email_to, email_subject, email_html = email_data

    email_data = {'from': email_from,
            'to': email_to,
            'subject': email_subject,
            'html': email_html}
    request = requests.post(request_url,
        auth=('api', key),
        data=email_data)

    print 'Status: {0}'.format(request.status_code)
    print 'Body:   {0}'.format(request.text)


def preview_email(request, email_data):
    if 'submit' not in request.POST:
        print 'preview mode'
        email_from, email_to, email_subject, email_html = email_data
        body_no_html = strip_html(email_html)
        template_name = 'students/emails/email_preview.html'
        context = {'form': EditEmailForm(initial={
                                            'to': email_to,
                                            'subject': email_subject,
                                            'body_as_html': email_html,
                                            'body_no_html': body_no_html}),
                   'from': email_from,
                   'html': email_html
            }

    elif request.POST['submit'] == 'send_edited':
        form = EditEmailForm(request.POST)
        if form.is_valid():
            email_data = ('LEARNBUZZY Mrs. K.<dee@deekras.com>',
                          cleaned_data['to'],
                          cleaned_data['subject'],
                          cleaned_data['body_as_html']
            )
    elif request.POST['submit'] == 'send_original':
        email_data = ('LEARNBUZZY Mrs. K.<dee@deekras.com>',
                         request.session['to'],
                         request.session['subject'],
                         request.session['body_as_html']
            )
        return send_email(email_data)
    print 'referer', request.META.get('HTTP_REFERER')
    print request.POST

    return render(request, template_name, context)

def edited_email(request):
#     print 'referer', request.META.get('HTTP_REFERER')
    pass
#     if request.POST['submit'] == 'send_edited':
#         print 'send edited'
#         form = EditEmailForm(request.POST)
#         print 'form data {}'.format(form.data['submit'])
#         if form.is_valid():
#             print 'valid'
#             email_data = ('LEARNBUZZY Mrs. K.<dee@deekras.com>',
#                           cleaned_data['to'],
#                           cleaned_data['subject'],
#                           cleaned_data['body_as_html']
#             )
#             print email_data
#             return send_email(email_data)
#         else:
#             print 'not valid'
#     elif request.POST['submit'] == 'send_original':
#         email_data = ('LEARNBUZZY Mrs. K.<dee@deekras.com>',
#                          request.session['to'],
#                          request.session['subject'],
#                          request.session['body_as_html']
#             )
#         return send_email(email_data)
    #redirect to student's edit page