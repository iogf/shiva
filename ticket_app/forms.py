from captcha.fields import ReCaptchaField
from ticket_app.models import Ticket, TicketReport
from django import forms
from django.conf import settings

class TicketForm(forms.ModelForm):
    # To get automated tests working. It seems ReCaptchaField doesn't
    # work as expected with required=False.

    captcha = forms.CharField(disabled=True, required=False,
    help_text='Google Captcha.') if settings.NOCAPTCHA \
    else ReCaptchaField() 

    class Meta:
        model   = Ticket
        exclude = ('enabled', )

class FindTicketForm(forms.Form):
    ITEM_TYPE_CHOICES = (('', '------'), ('0', 'Food'), 
    ('1','Medical'), ('2','Shelter'), ('3','Utils/Clothes'))

    TYPE_CHOICES = (('', '------'), ('0', 'Help'),('1','Helper'))

    keywords = forms.CharField(required=False, 
    help_text='Example: aspirins antibiotics')

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
