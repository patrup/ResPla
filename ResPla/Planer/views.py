from django.views.generic.edit import CreateView
from django.views.generic import ListView
from Planer.models import Resource, Booking


class IndexView(ListView):
    template_name = 'Planer/index.html'

    def get_queryset(self):
        return Booking.objects.all()
    
    
class AddResourceView(CreateView):
    """Adds a new resource"""
    #uses template resource_form.html
    model = Resource
    fields = ['title', 'cost']
    success_url = '/planer/resource_list/'
    

class ResourceListView(ListView):
    
    def get_queryset(self):
        return Resource.objects.all()