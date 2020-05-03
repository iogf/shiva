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
    null=True, blank=False, unique=True)

    CHOICES = (
        ('0', 'Help'),
        ('1','Helper'),
    )

    type = models.CharField(max_length=6, 
    verbose_name='Type', help_text='Are you an angel?', 
    choices=CHOICES, default='1')

    enabled = models.BooleanField(default=False)
