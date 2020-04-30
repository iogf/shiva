from django.shortcuts import render
from django.views.generic import View
from . import models

# Create your views here.
class ListTickets(View):
    def get(self, request):
        return render(request, 
            'ticket_app/list-tickets.html', {})

class CreateTicket(View):
    def get(self, request):
        return render(request, 
            'ticket_app/create-ticket.html', {})

    def post(self, request):
        pass

class DeleteTicket(View):
    def post(self, request):
        pass

class EnableTicket(View):
    def post(self, request):
        pass

class CloseTicket(View):
    def post(self, request):
        pass

class FindTicket(View):
    def get(self, request):
        return render(request, 
            'ticket_app/find-tickets.html', {})

    def post(self, request):
        pass





    
