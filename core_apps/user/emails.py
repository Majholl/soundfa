from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task



@shared_task
def send_reset_password_code_email(email, username, code):
    subject = ('Your reset passowrd code')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    context = {
        'username' : username,
        'code': code,
        'site_name': settings.SITE_NAME,
        'admin_email': settings.ADMIN_EMAIL}
    
    html_email = render_to_string('emails/reset_password.html', context=context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   
    
    try:
        email.send()
    except Exception as err:
        print(err)