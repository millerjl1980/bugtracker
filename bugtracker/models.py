from django.db import models
from django.conf import settings
from datetime import datetime

from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    display_name = models.CharField(max_length=50, null=True, blank=True)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    filed_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='filed_by')
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='assigned_to', null=True,blank=True, default=None)
    completed_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='completed_by', blank=True, default=None)

    # https://stackoverflow.com/questions/2771676/django-datetime-issues-default-datetime-now
    time_submitted = models.DateTimeField(default=datetime.now)

    new = 'n'
    inprog = 'p'
    done = 'd'
    invalid = 'na'

    status_choices = {
        (new, 'New'),
        (inprog, 'In-Progress'),
        (done, 'Done'),
        (invalid, 'Invalid'),
    }

    ticket_status = models.CharField(
        max_length=10,
        choices=status_choices,
        default=new,
    )

    def __str__(self):
        return self.title