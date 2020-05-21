from captcha.fields import ReCaptchaField
from django import forms
from .models import Ticket, TicketReport

class TicketForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model   = Ticket
        exclude = ('enabled', )

class FindTicketForm(forms.Form):
    ITEM_TYPE_CHOICES = (('', '------'), ('0', 'Food'), 
    ('1','Medical'), ('2','Shelter'), ('3','Utils/Clothes'))

    TYPE_CHOICES = (('', '------'), ('0', 'Help'),('1','Helper'))

    name = forms.CharField(required=False, 
    help_text='Example: Tau')

    type = forms.ChoiceField(required=False, 
    choices=TYPE_CHOICES)

    item_type = forms.ChoiceField(required=False, 
    choices=ITEM_TYPE_CHOICES)

    country = forms.CharField(required=False, 
    help_text='Example: India')

    state = forms.CharField(required=False, 
    help_text='Example: RJ')

    city = forms.CharField(required=False, 
    help_text='Example: Rio')

    email = forms.EmailField(required=False, 
    help_text='Example: last.src@gmail.com')

class DeleteTicketForm(forms.Form):
    pass

class TicketReportForm(forms.ModelForm):
    class Meta:
        model   = TicketReport
        exclude = ()
