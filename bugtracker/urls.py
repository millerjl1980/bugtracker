from django.urls import path
from bugtracker import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('add_user.html', views.add_user, name='add_user'),
]