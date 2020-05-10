from django.urls import path

from . import views

urlpatterns = [
    path('list-tickets/', views.ListTickets.as_view(), name='list-tickets'),
    path('enable-ticket/<int:ticket_id>/', views.EnableTicket.as_view(), name='enable-ticket'),
    path('ticket-matches/<int:ticket_id>/', views.TicketMatches.as_view(), name='ticket-matches'),
    path('create-ticket/', views.CreateTicket.as_view(), name='create-ticket'),
    path('find-ticket/', views.FindTicket.as_view(), name='find-ticket'),
    path('validate-email/', views.ValidateEmail.as_view(), name='validate-email'),

]

app_name = 'ticket_app'