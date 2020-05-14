from django.shortcuts import render, redirect
from django.views.generic import View
from .models import TicketToken, Ticket
from . import forms
import secrets

# Create your views here.
class ListTickets(View):
    def get(self, request):
        tickets = Ticket.objects.filter(enabled=True)
        tickets = tickets.order_by('-created')

        return render(request, 
            'ticket_app/list-tickets.html', {'tickets': tickets})

class TicketMatches(View):
    def get(self, request, ticket_id):
        ticket  = Ticket.objects.get(id=ticket_id)
        matches = Ticket.ticket_matches(ticket)
        matches = matches.order_by('-created')

        return render(request, 
            'ticket_app/ticket-matches.html', {'matches': matches})

class EnableTicket(View):
    def get(self, request, ticket_id):
        c_helper = Ticket.objects.filter(type='1', enabled=True)
        c_help   = Ticket.objects.filter(type='0', enabled=True)
        c_helper = c_helper.count()
        c_help   = c_help.count()

        return render(request, 
            'ticket_app/enable-ticket.html', {'c_helper': c_helper, 
                'c_help': c_help, 'ticket_id': ticket_id})

class ValidateEmail(View):
    def get(self, request, ticket_id, token):
        token  = TicketToken.objects.get(token=token, ticket__id=ticket_id)
        token.ticket.enabled=True
        token.ticket.save()
        # token.delete()

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

        token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=ticket)

        token.send_token()
        return redirect('ticket_app:enable-ticket', 
        ticket_id=ticket.id)

class DeleteTicket(View):
    def get(self, request, ticket_id, token):
        # token  = TicketToken.objects.get(token=token, ticket__id=ticket_id)
        ticket = Ticket.objects.get(id=ticket_id, token__token=token)
        token  = ticket.token.first()

        return render(request, 'ticket_app/delete-ticket.html', 
            {'ticket': ticket, 'token': token.token})

    def post(self, request, ticket_id, token):
        form = forms.DeleteTicketForm(request.POST)
        ticket = Ticket.objects.get(id=ticket_id, token__token=token)
        token  = ticket.token.first()

        if not form.is_valid():
            return render(request, 'ticket_app/delete-ticket.html', 
                {'ticket': ticket, 'token': token.token})

        ticket.delete()
        return redirect('ticket_app:list-tickets')

# class CloseTicket(View):
    # def post(self, request):
        # pass

class FindTicket(View):
    def get(self, request):
        form = forms.FindTicketForm()

        return render(request, 
            'ticket_app/find-ticket.html', {'form': form})

    def post(self, request):
        form = forms.FindTicketForm(request.POST)

        if not form.is_valid():
            return render(request, 'ticket_app/find-ticket.html', 
                    {'form': form}, status=400)

        fields  = form.cleaned_data.items()
        fields  = dict(fields)
        records = Ticket.find(**fields)
        records = tickets.order_by('-created')

        return render(request, 
            'ticket_app/found-ticket.html', {'tickets': records})


