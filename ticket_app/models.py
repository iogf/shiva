from django.db import models

# Create your models here.
class TicketMixin(models.Model):
    class Meta:
        abstract = True

class Ticket(TicketMixin):
    enabled = models.BooleanField(default=False)
