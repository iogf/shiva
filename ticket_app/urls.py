from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTickets.as_view(), name='list-tickets'),
]

app_name = 'ticket_app'