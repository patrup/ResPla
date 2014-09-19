from django.views.generic.edit import CreateView
from django.views.generic import ListView
from Planer.models import Resource, Booking


class IndexView(ListView):
    template_name = 'Planer/index.html'

    def get_queryset(self):
        return Booking.objects.all()
    
    
class AddResourceView(CreateView):
    model = Resource
    fields = ['title', 'cost']
    
