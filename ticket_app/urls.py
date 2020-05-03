from django.urls import path

from . import views

urlpatterns = [
    path('list-tickets', views.ListTickets.as_view(), name='list-tickets'),
    path('enable-ticket', views.EnableTicket.as_view(), name='enable-ticket'),
    path('create-ticket', views.CreateTicket.as_view(), name='create-ticket'),
    path('find-tickets', views.FindTickets.as_view(), name='find-tickets'),
    path('validate-email', views.ValidateEmail.as_view(), name='validate-email'),

]

app_name = 'ticket_app'