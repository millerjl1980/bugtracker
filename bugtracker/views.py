from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from bugtracker.forms import AddTicketForm, LoginForm, AddUserForm, EditTicketForm
from bugtracker.models import Ticket, MyUser

# Create your views here.
@login_required
def home(request):
    n_tickets = Ticket.objects.filter(ticket_status='n')
    ip_tickets = Ticket.objects.filter(ticket_status='p')
    d_tickets = Ticket.objects.filter(ticket_status='d')
    return render(request, 'home.html',
                  {'n_tickets': n_tickets,
                  'ip_tickets': ip_tickets,
                  'd_tickets': d_tickets})

@login_required
def ticket(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    return render(request, 'ticket.html', {'ticket': ticket})

@login_required
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

@login_required
def user(request, id):
    user = get_object_or_404(MyUser, pk=id)
    # Got help from Peter on 5/7 for redering and sorting recipes
    a_tickets = Ticket.objects.filter(assigned_to=user)
    f_tickets = Ticket.objects.filter(filed_by=user)
    c_tickets = Ticket.objects.filter(completed_by=user)
    return render(request, 'user.html', {'user': user, 
                                        'a_tickets': a_tickets,
                                        'c_tickets': c_tickets,
                                        'f_tickets': f_tickets})

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

@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            ticket.refresh_from_db()
            id = ticket.id
            return HttpResponseRedirect(reverse('ticket', args=(id,)))
    else:
        form = AddTicketForm()
    return render(request, 'generic_form.html', {'form': form})

@login_required
def ticket_edit(request, id):
    ticket = get_object_or_404(Ticket, pk=id)
    if request.method == "POST":
        form = EditTicketForm(request.POST, instance=ticket)
        form.save()
        if form.cleaned_data['assigned_to'] != None:
            ticket.ticket_status = 'p'
            ticket.completed_by = None
            ticket.assigned_to = form.cleaned_data['assigned_to']
            ticket.save()
        form_status = form.cleaned_data['ticket_status']
        if form_status == 'na':
            ticket.completed_by = None
            ticket.assigned_to = None
            ticket.save()
        if form_status == 'd':
            ticket.ticket_status = 'd'
            ticket.completed_by = form.cleaned_data['assigned_to']
            ticket.assigned_to = None
            ticket.save()
        return HttpResponseRedirect(reverse('ticket', args=(id,)))

    form = EditTicketForm(instance=ticket)
    return render(request, 'generic_form.html', {'form': form})