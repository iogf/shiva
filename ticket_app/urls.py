from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTickets.as_view(), name='list-tickets'),
    path('', views.CreateTicket.as_view(), name='create-ticket'),
    path('', views.FindTicket.as_view(), name='find-ticket'),


]

app_name = 'ticket_app'