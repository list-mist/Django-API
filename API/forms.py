from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms

class userForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password=forms.PasswordInput()
    confirm_password=forms.PasswordInput()
    class Meta:
        model = User
        fields=('username','email','password1','password2')

class EditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','is_staff','is_active','date_joined','last_login']
    