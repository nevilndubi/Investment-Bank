from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label= "", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), help_text='Required. Inform your first name.')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), help_text='Required. Inform your Last name.')