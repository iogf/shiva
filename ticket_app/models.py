from django.db import models
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
    def find(cls, type=None, item_type=None, name=None, phone=None, 
        email=None, description=None, country=None, city=None, enabled=True):

        records = cls.objects.filter(enabled=enabled)
        if city:
            records = records.filter(city__icontains=city)

        if type:
            records = records.filter(type=type)
        if item_type:
            records = records.filter(item_type=item_type)
        if name:
            records = records.filter(name__icontains=name)
        if description:
            records = records.filter(description__icontains=description)
        if phone:
            records = records.filter(phone=phone)

        if country:
            records = records.filter(country__icontains=country)
        if email:
            records = records.objects.filter(email=email)

        return records

    def ticket_url(self):
        url = reverse('ticket_app:load-ticket', kwargs={
        'ticket_id': self.id})

        url = '%s%s' % (settings.SITE_ADDRESS, url)
        return url

    def ticket_matches(self):
        type = '0' if self.type == '1' else '1'
        records = self.__class__.objects.filter(type=type, item_type=self.item_type,
        country=self.country, city=self.city, enabled=True)
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
        'Link to avoid ticket expiration\n%s\n\n'
        'Your ticket will expire on %s\n')

        message = message % (url0, url1, 
        self.ticket.expiration, url2)

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.ticket.email,]

        send_mail(subject, message, email_from, recipient_list)

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
    blank=False, verbose_name='City', 
    help_text='Type your city.', max_length=60)

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

