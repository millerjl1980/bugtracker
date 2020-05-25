from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    display_name = models.CharField(max_length=50, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    # https://stackoverflow.com/questions/15988183/cant-create-super-user-with-custom-user-model-in-django-1-5
    age = models.IntegerField(null=True)

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    filed_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    completed_by = models.CharField(max_length=100)
    time_submitted = models.DateTimeField()
    status_choices = {
        ('new', 'New'),
        ('inprog', 'In-Progress'),
        ('done', 'Done'),
        ('invalid', 'Invalid'),
    }
    ticket_status = models.CharField(
        max_length=10,
        choices=status_choices,
        default='new',
    )

    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title