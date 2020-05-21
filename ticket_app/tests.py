from django.test import TestCase, Client
from ticket_app.models import Ticket, TicketToken
from django.conf import settings
from datetime import date
from django.urls import reverse

# Create your tests here.

class TicketUrlMT(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='Zarathustra', 
        phone='22 4123321', email='last.src@gmail.com', note='Pls', 
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today())

    def test(self):
        url0 = self.ticket.ticket_url()
        url1 = reverse('ticket_app:load-ticket', kwargs={
        'ticket_id': self.ticket.id})

        url1 = '%s%s' % (settings.SITE_ADDRESS, url1)

        self.assertEqual(url0, url1)

class FindMT(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='Zarathustra', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

    def test(self):
        records = Ticket.find(name='Zara')
        self.assertIn(self.ticket, records)

        records = Ticket.find(type='0')
        self.assertIn(self.ticket, records)

        records = Ticket.find(phone='22 4123321')
        self.assertIn(self.ticket, records)

        records = Ticket.find(email='last.src@gmail.com')
        self.assertIn(self.ticket, records)

        records = Ticket.find(item_type='0')
        self.assertIn(self.ticket, records)

        records = Ticket.find(country='BRAZ')
        self.assertIn(self.ticket, records)

        records = Ticket.find(state='rj')
        self.assertIn(self.ticket, records)

        records = Ticket.find(city='rio')
        self.assertIn(self.ticket, records)

