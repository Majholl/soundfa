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
        pass
       
       
       
       
        
@shared_task
def confirmation_reset_password_email(email, username):
    subject = ('Confirmation reset password.')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    context = {
        'username' : username,
        'site_name': settings.SITE_NAME,
        'admin_email': settings.ADMIN_EMAIL}
    
    html_email = render_to_string('emails/confirmation_password_reset.html', context=context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   
    
    try:
        email.send()
    except Exception as err:
        print(err)
   
   
   
   
   
        
@shared_task
def send_otp_link_email(email, username, otp_link):
    subject = ('OTP verification.')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    context = {
        'username' : username,
        'site_name': settings.SITE_NAME,
        'url' : otp_link, 
        'admin_email': settings.ADMIN_EMAIL}
    
    html_email = render_to_string('emails/otp_registration.html', context=context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   
    
    try:
        email.send()
    except Exception as err:
        print(err)
      
      
        
        
        
        
@shared_task
def send_confirmation_otp_email(email, username):
    subject = ('OTP verification.')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    context = {
        'username' : username,
        'site_name': settings.SITE_NAME,
        'admin_email': settings.ADMIN_EMAIL}
    
    html_email = render_to_string('emails/otp_verified.html', context=context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   
    
    try:
        email.send()
    except Exception as err:
        print(err)