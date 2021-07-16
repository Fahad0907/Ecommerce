from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import Profile


class RegistrationFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'phone']
        labels = {
            'full_name': 'Full Name',
            'address': 'Address',
            'phone': 'Phone',
        }
