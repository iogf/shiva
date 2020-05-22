from django.core.management import BaseCommand
from django.db.models import Q
from ticket_app.models import Ticket, TicketToken
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = timezone.now().today().date()
        records = Ticket.objects.filter(expiration__lte=now)

        records.delete()
        self.stdout.write('Checked expiration!')
    

    







