from django import forms
from .models import Ticket
from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        model   = Ticket
        exclude = ('enabled', )

class FindTicketForm(forms.Form):
    name = forms.CharField(required=False, 
    help_text='Example: Tau')

    type = forms.ChoiceField(required=True, 
    choices=Ticket.TYPE_CHOICES)

    item = forms.ChoiceField(required=True, 
    choices=Ticket.ITEM_CHOICES)

    email = forms.EmailField(required=False, 
    help_text='Example: last.src@gmail.com')




