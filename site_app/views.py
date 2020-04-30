from django.shortcuts import render
from django.views.generic import View
from ticket_app.models import Ticket

# Create your views here.
class Index(View):
    def get(self, request):
        count = Ticket.objects.count()
        return render(request, 
            'site_app/index.html', {'count': count})
