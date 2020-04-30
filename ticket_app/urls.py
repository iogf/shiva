from django.urls import path

from . import views

urlpatterns = [
    path('list-tickets', views.ListTickets.as_view(), name='list-tickets'),
    path('create-ticket', views.CreateTicket.as_view(), name='create-ticket'),
    path('find-ticket', views.FindTicket.as_view(), name='find-ticket'),


]

app_name = 'ticket_app'