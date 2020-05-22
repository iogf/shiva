from django.shortcuts import render, redirect
from django.views.generic import View
from .models import TicketToken, Ticket
from django.core.mail import send_mail, mail_admins
from django.conf import settings
from datetime import date, timedelta
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
        ticket = Ticket.objects.get(id=ticket_id)

        c_helper = Ticket.objects.filter(type='1', enabled=True)
        c_help   = Ticket.objects.filter(type='0', enabled=True)
        c_helper = c_helper.count()
        c_help   = c_help.count()

        return render(request, 
            'ticket_app/enable-ticket.html', {'c_helper': c_helper, 
                'c_help': c_help, 'ticket': ticket})

class AvoidExpiration(View):
    def get(self, request, ticket_id, token):
        ticket = Ticket.objects.get(id=ticket_id)
        delta = timedelta(days=settings.TICKET_EXPIRATION)

        ticket.expiration = date.today() + delta
        ticket.save()

        return render(request, 
            'ticket_app/avoid-expiration.html', {'ticket': ticket})

class ValidateEmail(View):
    def get(self, request, ticket_id, token):
        token  = TicketToken.objects.get(token=token, ticket__id=ticket_id)
        token.ticket.enabled=True
        token.ticket.save()

        emails  = token.ticket.ticket_matches()
        emails  = emails.filter(alert_me=True)
        emails  = emails.distinct()
        emails  = emails.values_list('email', flat=True)
        url     = token.ticket.ticket_url()
        message = 'Check this new ticket!\n %s'
        subject = 'Shiva New Ticket!'

        message = message % url

        send_mail(subject, message, settings.EMAIL_FROM, emails)
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

        ticket = form.save(commit=False)
        delta  = timedelta(settings.TICKET_EXPIRATION)
        ticket.expiration = date.today() + delta
        ticket.save()

        token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=ticket)

        token.send_token()
        return redirect('ticket_app:enable-ticket', 
        ticket_id=ticket.id)

class DeleteTicket(View):
    def get(self, request, ticket_id, token):
        token  = TicketToken.objects.get(token=token, ticket__id=ticket_id)

        return render(request, 'ticket_app/delete-ticket.html', 
            {'ticket': token.ticket, 'token': token.token})

    def post(self, request, ticket_id, token):
        form   = forms.DeleteTicketForm(request.POST)
        token  = TicketToken.objects.get(token=token, ticket__id=ticket_id)

        if not form.is_valid():
            return render(request, 'ticket_app/delete-ticket.html', 
                {'ticket': token.ticket, 'token': token.token})

        token.ticket.delete()
        return redirect('ticket_app:list-tickets')

class ReportTicket(View):
    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form   = forms.TicketReportForm(request.POST)

        return render(request, 'ticket_app/report-ticket.html', 
            {'ticket': ticket, 'form': form})


    def post(self, request, ticket_id):
        form   = forms.TicketReportForm(request.POST)
        ticket = Ticket.objects.get(id=ticket_id)

        if not form.is_valid():
            return render(request, 'ticket_app/report-ticket.html', 
                {'ticket': ticket, 'form': form})
        report = form.save()

        message = ('This ticket %s was reported.\n\n%s\n\n' 
        'Report ID: %s') % (ticket.ticket_url(), report.reason, report.id)

        mail_admins('Ticket Report.', message)
        return redirect('ticket_app:list-tickets')

class LoadTicket(View):
    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)

        return render(request, 'ticket_app/load-ticket.html', 
            {'ticket': ticket})

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

        fields   = form.cleaned_data.items()
        fields   = dict(fields)
        keywords = fields.get('keywords') 

        fields['keywords'] = keywords.split(' ')
        records = Ticket.find(**fields)
        records = records.order_by('-created')

        return render(request, 
            'ticket_app/found-ticket.html', {'tickets': records})


