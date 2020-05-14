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
    def find(cls, type=None, item=None, name=None, phone=None, email=None, 
        description=None, country=None, city=None, enabled=True):

        records = cls.objects.filter(enabled=enabled)
        if city:
            records = records.filter(city__icontains=city)

        if type:
            records = records.filter(type=type)
        if item:
            records = records.filter(item=item)
        if name:
            records = records.filter(name__icontains=name)

        if description:
            records = records.filter(
                description__icontains=description)
        if phone:
            records = records.filter(phone=phone)

        if country:
            records = records.filter(
                country__icontains=country)
        if email:
            records = records.objects.filter(email=email)

        return records

    def ticket_matches(self):
        type = '0' if self.type == '1' else '1'
        records = self.__class__.objects.filter(type=type, item=self.item,
        country=self.country, city=self.city, enabled=True)
        return records

class Ticket(TicketMixin):
    name = models.CharField(null=False,
    blank=False, verbose_name='Name', 
    help_text='Type your name.', max_length=256)

    phone = models.CharField(null=True,
    blank=True, verbose_name='Phone', 
    help_text='Type your phone.', max_length=256)

    email = models.EmailField(max_length=70, 
    verbose_name='E-mail', help_text='E-mail for contact.', 
    null=False, blank=False)

    TYPE_CHOICES = (('0', 'Help'),('1','Helper'))

    type = models.CharField(max_length=6, 
    verbose_name='Type', help_text='Are you an angel?', 
    choices=TYPE_CHOICES, default='1')

    ITEM_CHOICES = (('0', 'Food'), ('1','Medical'),
    ('2','Shelter'), ('3','Clothes'))

    item = models.CharField(max_length=6, 
    verbose_name='Item', choices=ITEM_CHOICES, default='1',
    help_text='What is it that you have/need?')

    description = models.TextField(null=True,
    blank=False, verbose_name='Description', 
    help_text='Type a description/note.')

    # country = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)
    # city = models.ForeignKey(City, verbose_name='Country/City', 
    # help_text='Where can you give/receive help?',
    # on_delete=models.CASCADE, default=None)

    country = models.CharField(null=False,
    blank=False, verbose_name='Country', 
    help_text='Type your country.', max_length=256)

    city = models.CharField(null=True,
    blank=False, verbose_name='City', 
    help_text='Type your city.', max_length=256)

    created = models.DateTimeField(auto_now_add=True, null=True)
    enabled = models.BooleanField(default=False)

class TicketTokenMixin(models.Model):
    class Meta:
        abstract = True

    def send_token(self):
        query = reverse('ticket_app:validate-email', kwargs={
        'ticket_id': self.ticket.id, 'token': self.token})
        url = '%s%s' % (settings.SITE_ADDRESS, query)

        subject = 'Validate your Shiva ticket.'
        message = 'Click on the link to validate your ticket.\n%s'
        message = message % url

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.ticket.email,]

        send_mail(subject, message, email_from, recipient_list)

class TicketToken(TicketTokenMixin):
    token = models.CharField(null=False,
    blank=False, max_length=24)

    ticket = models.ForeignKey('Ticket', null=False, 
    related_name='token', on_delete=models.CASCADE)

