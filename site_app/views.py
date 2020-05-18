from django.shortcuts import render
from django.views.generic import View
from ticket_app.models import Ticket

# Create your views here.
class Index(View):
    def get(self, request):
        records = Ticket.objects.filter(enabled=True)
        count = records.count()

        return render(request, 
            'site_app/index.html', {'count': count})
