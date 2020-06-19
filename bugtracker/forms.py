from django import forms
from django.forms import modelform_factory
from bugtracker.models import Ticket

AddTicketForm = modelform_factory(Ticket, exclude=[])



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)