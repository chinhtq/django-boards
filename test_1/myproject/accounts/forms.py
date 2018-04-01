# -*- coding: UTF-8 -*-
# System libraries
from __future__ import unicode_literals
# Third-party libraries

# Django modules
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Current-app modules

# Other-app modules

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']