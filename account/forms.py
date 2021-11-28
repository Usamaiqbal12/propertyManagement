from django.db import models
from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'email','username', 'password1','password2']