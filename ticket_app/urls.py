from django.urls import path

from . import views

urlpatterns = [
    path('list-tickets/', views.ListTickets.as_view(), name='list-tickets'),
    path('enable-ticket/<int:ticket_id>/', views.EnableTicket.as_view(), name='enable-ticket'),
    path('report-ticket/<int:ticket_id>/', views.ReportTicket.as_view(), name='report-ticket'),
    path('load-ticket/<int:ticket_id>/', views.LoadTicket.as_view(), name='load-ticket'),

    path('delete-ticket/<int:ticket_id>/<str:token>/', views.DeleteTicket.as_view(), name='delete-ticket'),
    path('ticket-matches/<int:ticket_id>/', views.TicketMatches.as_view(), name='ticket-matches'),
    path('create-ticket/', views.CreateTicket.as_view(), name='create-ticket'),
    path('find-ticket/', views.FindTicket.as_view(), name='find-ticket'),
    path('validate-email/<int:ticket_id>/<str:token>/', views.ValidateEmail.as_view(), name='validate-email'),
    path('avoid-expiration/<int:ticket_id>/<str:token>/', views.AvoidExpiration.as_view(), name='avoid-expiration'),

]

app_name = 'ticket_app'