from django import forms
from django.forms import modelform_factory
from django.contrib.auth.forms import UserCreationForm
from bugtracker.models import Ticket, MyUser

AddTicketForm = modelform_factory(Ticket, exclude=[])

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class AddUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'display_name', 
                  'username', 'password1', 'password2')