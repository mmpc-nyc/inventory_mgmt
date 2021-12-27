from django import forms
from django.forms import Form
from django.forms import ValidationError


class LoginForm(Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
