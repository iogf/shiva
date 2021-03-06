from django.db import models
from django.db.models import Q
from urllib.parse import urljoin
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# from cities_light.models import City

# Create your models here.
class TicketMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return '%s - %s' % (self.name, self.email)

    @classmethod
    def find(cls, type=None, item_type=None, name=None, 
        phone=None, email=None, country=None, state=None, city=None,
        enabled=True, keywords=[]):

        records = cls.objects.filter(enabled=enabled)
        if city:
            records = records.filter(city__icontains=city)

        if type:
            records = records.filter(type=type)
        if item_type:
            records = records.filter(item_type=item_type)
        if name:
            records = records.filter(name__icontains=name)

        if phone:
            records = records.filter(phone=phone)

        if country:
            records = records.filter(country__icontains=country)

        if state:
            records = records.filter(state__icontains=state)

        if email:
            records = records.filter(email=email)

        qwords = Q()
        for ind in keywords:
            qwords = qwords | Q(note__icontains=ind)

        records = records.filter(qwords)
        return records

    def ticket_url(self):
        url = reverse('ticket_app:load-ticket', kwargs={
        'ticket_id': self.id})

        url = '%s%s' % (settings.SITE_ADDRESS, url)
        return url

    def ticket_matches(self):
        type = '0' if self.type == '1' else '1'
        query = Q(type=type, item_type=self.item_type,
        country=self.country, state=self.state, enabled=True)

        if self.city and self.type=='0':
            query = query & Q(city=self.city)

        records = self.__class__.objects.filter(query)
        return records

class TicketTokenMixin(models.Model):
    class Meta:
        abstract = True

    def delete_url(self):
        url = reverse('ticket_app:delete-ticket', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token})
        url = '%s%s' % (settings.SITE_ADDRESS, url)

        return url

    def vmail_url(self):
        url = reverse('ticket_app:validate-email', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token})
        url = '%s%s' % (settings.SITE_ADDRESS, url)

        return url

    def expiration_url(self):
        url = reverse('ticket_app:avoid-expiration', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token})
        url = '%s%s' % (settings.SITE_ADDRESS, url)

        return url

    def send_token(self):
        url0 = self.vmail_url()
        url1 = self.delete_url()
        url2 = self.expiration_url()

        subject = 'Validate your Shiva ticket.'
        message = ('Click on the link to validate your ticket.\n%s\n\n'
        'Use this link to delete your ticket.\n%s\n\n'
        'Link to avoid ticket expiration on %s\n\n'
        'Your ticket will expire on %s\n')

        message = message % (url0, url1, 
        self.ticket.expiration, url2)

        recipient_list = [self.ticket.email,]

        send_mail(subject, message, settings.EMAIL_FROM, recipient_list)

class TicketReportMixin(models.Model):
    class Meta:
        abstract = True

class Ticket(TicketMixin):
    name = models.CharField(null=False,
    blank=False, verbose_name='Name', 
    help_text='Type your name.', max_length=256)

    phone = models.CharField(null=True,
    blank=True, verbose_name='Phone', 
    help_text='Type your phone.', max_length=30)

    email = models.EmailField(max_length=70, 
    verbose_name='E-mail', help_text='E-mail for contact.', 
    null=False, blank=False)

    TYPE_CHOICES = (('0', 'Need help!'),('1','Can help!'))

    type = models.CharField(max_length=6, 
    verbose_name='Type', help_text='Are you an angel?', 
    choices=TYPE_CHOICES, default='1')

    ITEM_TYPE_CHOICES = (('0', 'Food'), ('1','Medical'),
    ('2','Shelter'), ('3','Utils/Clothes'))

    item_type = models.CharField(max_length=6, 
    verbose_name='Item Type', choices=ITEM_TYPE_CHOICES, default='1',
    help_text='What is it that you have/need?')

    note = models.TextField(null=True,
    blank=False, verbose_name='Note', 
    help_text='Type a note.')

    # country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)
    # city = models.ForeignKey(City, verbose_name='Country/City', 
    # help_text='Where can you give/receive help?',
    # on_delete=models.CASCADE, default=None)

    country = models.CharField(null=False,
    blank=False, verbose_name='Country', 
    help_text='Type your country.', max_length=60)

    state = models.CharField(null=True,
    blank=False, verbose_name='State', 
    help_text='Type your state.', max_length=60)

    city = models.CharField(null=True,
    blank=True, help_text='Type your city. (Optional)', 
    max_length=60, verbose_name='City')

    alert_me = models.BooleanField(blank=False, 
    null=False, default=True, verbose_name='Notifications', 
    help_text='Get E-mail notifications for new tickets?',)

    expiration = models.DateTimeField(blank=True, null=False)

    created = models.DateTimeField(auto_now_add=True, null=True)
    enabled = models.BooleanField(default=False)

class TicketToken(TicketTokenMixin):
    token = models.CharField(null=False,
    blank=False, max_length=24)

    ticket = models.ForeignKey('Ticket', null=False, 
    related_name='token', on_delete=models.CASCADE)

class TicketReport(TicketReportMixin):
    reason = models.TextField(null=False,
    blank=False, verbose_name='Reason', 
    help_text='Type a reason.')

