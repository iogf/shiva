from django import forms
from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        model   = models.Ticket
        exclude = ('enabled', )

class FindTicketForm(forms.Form):
    name = forms.CharField(required=False, 
    help_text='Example: Tau')

    email = forms.EmailField(required=False, 
    help_text='Example: last.src@gmail.com')




