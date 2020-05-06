from django.db import models

# Create your models here.
class TicketMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return '%s - %s' % (self.name, self.email)

class Ticket(TicketMixin):
    name = models.CharField(null=True,
    blank=False, verbose_name='Name', 
    help_text='Type your name.', max_length=256)

    email = models.EmailField(max_length=70, 
    verbose_name='E-mail', help_text='E-mail for contact.', 
    null=True, blank=False)

    TYPE_CHOICES = (('0', 'Help'),('1','Helper'))

    type = models.CharField(max_length=6, 
    verbose_name='Type', help_text='Are you an angel?', 
    choices=TYPE_CHOICES, default='1')

    ITEM_CHOICES = (('0', 'Food'), ('1','Medical'),
    ('2','Shelter'), ('3','Clothes'))

    item = models.CharField(max_length=6, 
    verbose_name='Item', choices=ITEM_CHOICES, default='1',
    help_text='What is it that you have/need?', 
)

    description = models.TextField(null=True,
    blank=False, verbose_name='Description', 
    help_text='Type a description/note.')

    enabled = models.BooleanField(default=False)
