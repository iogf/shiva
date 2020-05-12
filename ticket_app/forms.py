from captcha.fields import ReCaptchaField
from django import forms
from .models import Ticket
from . import models

class TicketForm(forms.ModelForm):
    captcha = ReCaptchaField()

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

    country = forms.CharField(required=False, 
    help_text='Example: India')

    city = forms.CharField(required=False, 
    help_text='Example: Rio')

    email = forms.EmailField(required=False, 
    help_text='Example: last.src@gmail.com')




