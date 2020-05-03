from django.shortcuts import render, redirect
from django.views.generic import View
from . import models
from . import forms

# Create your views here.
class ListTickets(View):
    def get(self, request):
        return render(request, 
            'ticket_app/list-tickets.html', {})

class EnableTicket(View):
    def get(self, request):
        c_helper = models.Ticket.objects.filter(type='1')
        c_help   = models.Ticket.objects.filter(type='0')
        c_helper = c_helper.count()
        c_help   = c_help.count()

        return render(request, 
            'ticket_app/enable-ticket.html', 
                {'c_helper': c_helper, 'c_help': c_help})

class CreateTicket(View):
    def get(self, request):
        form = forms.TicketForm()
        return render(request, 
            'ticket_app/create-ticket.html', {'form': form})

    def post(self, request):
        form = forms.TicketForm(request.POST)

        if not form.is_valid():
            return render(request, 'ticket_app/create-ticket.html', 
                    {'form': form}, status=400)
        form.save()
        return redirect('ticket_app:enable-ticket')

class DeleteTicket(View):
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





    
