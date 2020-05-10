from django.db import models
# from cities_light.models import City

# Create your models here.
class TicketMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return '%s - %s' % (self.name, self.email)

    def ticket_matches(self):
        type = '0' if self.type == '1' else '1'
        records = self.__class__.objects.filter(type=type, item=self.item,
        country=self.country, city=self.city)
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

    enabled = models.BooleanField(default=False)
