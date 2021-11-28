from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from .tokens import token_generator
from django.utils.encoding import force_bytes, force_text
from .views import *
from django.core.mail import EmailMessage
import time
from propertymanagement import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

logger = get_task_logger(__name__)
User = get_user_model()
@shared_task
def send_confirmation_mail_task(user_id, random):
    print(random)
    user = User.objects.get(id=user_id)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = Site.objects.get_current().domain
    link = reverse('activate', args=[uidb64, token_generator.make_token(user)])
    activation_link = f'http://{current_site}{link}'
    email_subject = 'Activate your account'
    email_body = f'Hi {user.username} you have succesfully signed up by clicking \n {activation_link}'
    email_from = settings.EMAIL_HOST_USER
    email1 = EmailMessage(
        email_subject,
        email_body,
        email_from,
        [user.email]
        )
    email1.send()
    return 'Done'
    




# @shared_task(bind=True)
# def send_confirmation_mail_task(request,user):
#     logger.info("Sent Confirmation Email")
#     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#     domain = get_current_site(request).domain
#     link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
#     activation_link = f'http://{domain}{link}'
#     email_subject = 'Activate your account'
#     email_body = f'Hi {user.username} Please use this link to verify your account \n {activation_link}'
#     email = EmailMessage(
#         email_subject,
#         email_body,
#         'noreply@semycolon.com',
#         [user.email]
#         )
#     email.send(fail_silently=False)