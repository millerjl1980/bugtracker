from django.shortcuts import render
from bugtracker.forms import AddTicketForm
from bugtracker.models import Ticket

# Create your views here.
def home(request):
    return render(request, 'home.html',
                  {'tickets': Ticket.objects.all()})


def add_ticket(request):
    if request.method == 'POST':
        pass
    else:
        form = AddTicketForm()
    return render(request, 'add_ticket.html', {'form': form})