from django.test import TestCase, Client
from ticket_app.models import Ticket, TicketToken
from ticket_app.forms import TicketForm
from django.conf import settings
from django.core import mail
from datetime import date
from django.urls import reverse
import secrets

# Create your tests here.

class TicketUrlTM(TestCase):
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

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)

class FindTM(TestCase):
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

class TicketMatchesTM(TestCase):
    def setUp(self):
        self.ticket0 = Ticket.objects.create(name='Zarathustra', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.ticket1 = Ticket.objects.create(name='Tau', type='1',
        phone='22 4123321', email='sukhoi696@gmail.com', 
        note='Pls', item_type='0',country='Brazil', state='RJ', city='', 
        expiration=date.today(), enabled=True)

        self.ticket2 = Ticket.objects.create(name='UnknownSoldier', type='1',
        phone='22 29382', email='fuinho@gmail.com', 
        note='Pls', item_type='0',country='Brazil', state='RJ', city='', 
        expiration=date.today(), enabled=False)

        self.ticket3 = Ticket.objects.create(name='Ticiane', type='1',
        phone='22 112', email='perninhasdesaracura@gmail.com', 
        note='Pls', item_type='1',country='Brazil', state='RJ', city='', 
        expiration=date.today(), enabled=False)

        self.ticket4 = Ticket.objects.create(name='Rafaela', type='1',
        phone='22 29382', email='bobsponja@gmail.com', note='Pls', 
        item_type='0',country='Brazil', expiration=date.today(),
        state='RJ', city='Rio de Fevereiro', enabled=True)

        self.ticket5 = Ticket.objects.create(name='Foobar', type='1',
        phone='22 29382', email='foobar@gmail.com', note='Pls', 
        item_type='0',country='Brazil', expiration=date.today(),
        state='RJ', city='oooo', enabled=True)

    def test(self):
        records = self.ticket0.ticket_matches()
        self.assertNotIn(self.ticket1, records)

        records = self.ticket0.ticket_matches()
        self.assertNotIn(self.ticket2, records)

        records = self.ticket0.ticket_matches()
        self.assertNotIn(self.ticket3, records)

        records = self.ticket0.ticket_matches()
        self.assertIn(self.ticket4, records)

        records = self.ticket0.ticket_matches()
        self.assertNotIn(self.ticket5, records)

        records = self.ticket1.ticket_matches()
        self.assertIn(self.ticket0, records)


class DeleteUrlTTM(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='Zarathustra', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=self.ticket)

    def test(self):
        url0 = self.token.delete_url()

        url1 = reverse('ticket_app:delete-ticket', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token.token})
        url1 = '%s%s' % (settings.SITE_ADDRESS, url1)

        self.assertEqual(url0, url1)

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)

class VMailUrlTTM(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='alpha', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=self.ticket)

    def test(self):
        url0 = self.token.vmail_url()

        url1 = reverse('ticket_app:validate-email', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token.token})
        url1 = '%s%s' % (settings.SITE_ADDRESS, url1)

        self.assertEqual(url0, url1)

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)

class ExpirationUrlTTM(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='beta', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=self.ticket)

    def test(self):
        url0 = self.token.expiration_url()

        url1 = reverse('ticket_app:avoid-expiration', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token.token})
        url1 = '%s%s' % (settings.SITE_ADDRESS, url1)

        self.assertEqual(url0, url1)

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)

class SendTokenTTM(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='beta', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=self.ticket)

    def test(self):
        self.token.send_token()

        url0 = self.token.vmail_url()
        url1 = self.token.delete_url()
        url2 = self.token.expiration_url()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Validate your Shiva ticket.')
        self.assertIn(url0, mail.outbox[0].message().get_payload())
        self.assertIn(url1, mail.outbox[0].message().get_payload())
        self.assertIn(url2, mail.outbox[0].message().get_payload())

class ListTicketsV(TestCase):
    def setUp(self):
        self.ticket0 = Ticket.objects.create(name='beta', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.ticket1 = Ticket.objects.create(name='gamma', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

    def test(self):
        url = reverse('ticket_app:list-tickets', kwargs={})
        response = self.client.get(url)
        self.assertEqual(self.ticket0, response.context['tickets'][1])
        self.assertEqual(self.ticket1, response.context['tickets'][0])

class TicketMatchesV(TestCase):
    def setUp(self):
        self.ticket0 = Ticket.objects.create(name='beta', type='0',
        phone='22 4123321', email='last.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.ticket1 = Ticket.objects.create(name='gamma', type='1',
        phone='32 1332', email='foobar@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today(), enabled=True)

        self.ticket2 = Ticket.objects.create(name='foobar', type='0',
        phone='32 1332', email='ooooe@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='', 
        expiration=date.today(), enabled=True)

    def test(self):
        url = reverse('ticket_app:ticket-matches', 
        kwargs={'ticket_id': self.ticket0.id})

        response = self.client.get(url)
        self.assertIn(self.ticket1, response.context['matches'])

        url = reverse('ticket_app:ticket-matches', 
        kwargs={'ticket_id': self.ticket2.id})

        response = self.client.get(url)
        self.assertIn(self.ticket1, response.context['matches'])

class CreateTicketV(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='hehe', type='1',
        phone='22 4123321', email='test.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today())

    def test(self):
        payload = {'name':'hehe', 'type':'0',
        'phone':'22 4123321', 'email':'ooo.src@gmail.com', 'note':'Pls', 'item_type':'0',
        'country':'Brazil', 'state':'RJ', 'city':'Rio de Fevereiro', }

        url0 = reverse('ticket_app:create-ticket', kwargs={})

        response = self.client.post(url0, payload)
        ticket = Ticket.objects.filter(email='ooo.src@gmail.com')
        ticket = ticket.order_by('-created').first()

        url1 = reverse('ticket_app:enable-ticket', 
        kwargs={'ticket_id': ticket.id})
        self.assertIn(url1, response.url)

        self.assertEqual(len(mail.outbox), 1)
        token = ticket.token.first()
        url2 = token.vmail_url()
        url3 = token.delete_url()
        url4 = token.expiration_url()

        self.assertIn(url2, mail.outbox[0].message().get_payload())
        self.assertIn(url3, mail.outbox[0].message().get_payload())
        self.assertIn(url4, mail.outbox[0].message().get_payload())

        url5 = reverse('ticket_app:validate-email',
        kwargs={'ticket_id': ticket.id, 'token': token.token})

        response = self.client.get(url5)
        self.assertEqual(response.status_code, 200)

        # Make sure the ticket was enabled. The existing Ticket
        # instance is not updated in regard to the view workings.
        ticket = Ticket.objects.get(id=ticket.id)
        self.assertTrue(ticket.enabled)

class DeleteTicketV(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(name='hehe', type='0',
        phone='22 4123321', email='ooo.src@gmail.com', note='Pls', item_type='0',
        country='Brazil', state='RJ', city='Rio de Fevereiro', 
        expiration=date.today())

        self.token  = TicketToken.objects.create(
        token=secrets.token_urlsafe(24), ticket=self.ticket)

    def test(self):
        url = reverse('ticket_app:delete-ticket', 
        kwargs={'ticket_id': self.ticket.id, 'token': self.token.token})

        response = self.client.post(url, payload={})
