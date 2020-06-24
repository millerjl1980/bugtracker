from django.urls import path
from bugtracker import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('add_user.html', views.add_user, name='add_user'),
    path('user/<int:id>', views.user, name='user'),
    path('ticket/<int:id>', views.ticket, name='ticket'),
    path('add_ticket.html', views.add_ticket, name='add_ticket'),
    path('edit_ticket/<int:id>', views.ticket_edit, name='edit_ticket'),
]