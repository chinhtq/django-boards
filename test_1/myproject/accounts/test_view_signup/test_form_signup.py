# -*- coding: UTF-8 -*-
# System libraries
from __future__ import unicode_literals
from accounts.forms import SignUpForm
from django.test import TestCase
# Third-party libraries

# Django modules

# Current-app modules

# Other-app modules

class SignUpTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected,actual)