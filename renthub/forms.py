from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RenterSignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=10, required=True, help_text="Phone number:")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number']