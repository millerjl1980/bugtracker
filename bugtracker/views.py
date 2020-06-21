from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from bugtracker.forms import AddTicketForm, LoginForm, AddUserForm
from bugtracker.models import Ticket, MyUser

# Create your views here.
# @login_required
def home(request):
    return render(request, 'home.html',
                  {'tickets': Ticket.objects.all()})

def ticket(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    return render(request, 'ticket.html', {'ticket': ticket})

# @login_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = AddUserForm()
    return render(request, 'generic_form.html', {'form': form})

def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
                )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('home'))
                )
    form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})

def logoutview(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect(
                    request.GET.get('next', reverse('home'))
                )


def add_ticket(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddTicketForm()
    return render(request, 'generic_form.html', {'form': form})

def ticket_edit(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    if request.method == "POST":
        form = AddTicketForm(request.POST, instance=ticket)
        form.save()
        return HttpResponseRedirect(reverse('ticket', args=(id,)))

    form = AddTicketForm(instance=ticket)
    return render(request, 'generic_form.html', {'form': form})