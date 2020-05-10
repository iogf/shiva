from django.shortcuts import render, redirect
from django.views.generic import View
from . import models
from . import forms

# Create your views here.
class ListTickets(View):
    def get(self, request):
        tickets = models.Ticket.objects.all()
        return render(request, 
            'ticket_app/list-tickets.html', {'tickets': tickets})

class TicketMatches(View):
    def get(self, request, ticket_id):
        ticket  = models.Ticket.objects.get(id=ticket_id)
        matches = models.Ticket.ticket_matches(ticket)

        return render(request, 
            'ticket_app/ticket-matches.html', {'matches': matches})

class EnableTicket(View):
    def get(self, request, ticket_id):
        c_helper = models.Ticket.objects.filter(type='1')
        c_help   = models.Ticket.objects.filter(type='0')
        c_helper = c_helper.count()
        c_help   = c_help.count()

        return render(request, 
            'ticket_app/enable-ticket.html', {'c_helper': c_helper, 
                'c_help': c_help, 'ticket_id': ticket_id})

class ValidateEmail(View):
    def get(self, request):
        return render(request, 
            'ticket_app/validate-email.html', {})

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
        ticket = form.save()

        return redirect('ticket_app:enable-ticket', 
        ticket_id=ticket.id)

class DeleteTicket(View):
    def post(self, request):
        pass

class CloseTicket(View):
    def post(self, request):
        pass

class FindTicket(View):
    def get(self, request):
        form = forms.FindTicketForm()

        return render(request, 
            'ticket_app/find-ticket.html', {'form': form})

    def post(self, request):
        return render(request, 
            'ticket_app/found-ticket.html', {})





    
