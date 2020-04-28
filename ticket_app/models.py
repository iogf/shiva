from django.db import models

# Create your models here.
class TicketMixin(models.Model):
    class Meta:
        abstract = True

class Ticket(TicketMixin):
    name = models.CharField(null=True,
    blank=False, verbose_name='Name', 
    help_text='Name', max_length=256)

    email = models.EmailField(max_length=70, 
    null=True, blank=False, unique=True)

    enabled = models.BooleanField(default=False)
