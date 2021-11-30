from django.shortcuts import  redirect, render
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from django.urls import reverse
from .tokens import token_generator
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .tasks import send_confirmation_mail_task
from .forms import CreateUserForm
User = get_user_model()
# Create your views here.
def property_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form,
        'active_page': 'Login'
    }
    return render(request, 'accounts/login.html', context=context)

@login_required
def property_logout(request):
    if request.method =="POST":
        logout(request)
        return redirect(reverse("login"))
    return render(request,'accounts/logout.html', {})


def property_register(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save(commit=False)
        user_obj.is_active = False
        user_obj.save()
        # token = token_generator.make_token(user_obj)
        send_confirmation_mail_task.delay(user_obj.pk, 'hello world')
        return redirect(reverse("login"))
    context = {"form": form, "active_page": 'Register'}
    return render(request, 'accounts/register.html', context=context)

# def property_register(request):
#     form = CreateUserForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#         domain = get_current_site(request).domain
#         link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
#         activation_link = f'http://{domain}{link}'
#         email_subject = 'Activate your account'
#         email_body = f'Hi {user.username} Please use this link to verify your account \n {activation_link}'
#         email = EmailMessage(
#             email_subject,
#             email_body,
#             'noreply@semycolon.com',
#             [user.email]
#             )
#         email.send(fail_silently=False)
#         return redirect('/login')
#     else:
#         form = CreateUserForm()
#     context = {"form": form, "active_page": 'Register'}
#     return render(request, 'accounts/register.html', context=context)

# def property_register(request):
#     form = CreateUserForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         send_confirmation_mail_task.delay(request,user)

#     else:
#         form = CreateUserForm()
#     context = {"form": form, "active_page": 'Register'}
#     return render(request, 'accounts/register.html', context=context)

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    user = None
    # try:
    user_id = int(force_text(urlsafe_base64_decode(uidb64)))
    user = User.objects.get(id=user_id)
    # except (TypeError, ValueError, OverflowError, User.DoesNotExist,) as e:
        # print(e)
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend)
        return redirect(reverse("dashboard"))
    else:
        return HttpResponse("Activation link is invalid.") 
    

# def send_confirmation_mail(username, email):
#     user = User.objects.filter(email=email)
#     current_site = Site.objects.get_current().domain
#     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#     domain = current_site
#     link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
#     activation_link = f'http://{domain}{link}'
#     email_subject = 'Activate your account'
#     email_body = f'Hi {user.username} Please use this link to verify your account \n {activation_link}'
#     message={
#         'username': username,
#         'email': email,
#         'domain': current_site,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#         'token': token_generator.make_token(user),
#     }
#     email_subject = 'Activation Mail'
#     email_body = render_to_string('acc_active_email.html', message)

#     email = EmailMessage(
#             email_subject,
#             email_body,
#             'noreply@semycolon.com',
#             [user.email]
#     )
#     return email.send(fail_silently=False)