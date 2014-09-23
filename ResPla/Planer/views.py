import datetime
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from Planer.models import Resource, Booking, Person


class IndexView(ListView):
    template_name = 'Planer/index.html'

    def get_queryset(self):
        return Booking.objects.all()


class AddResourceView(CreateView):
    """Adds a new resource"""
    # uses template resource_form.html
    model = Resource
    fields = ['title', 'cost']
    success_url = '/planer/list/resource/'


class ResourceListView(ListView):

    def get_queryset(self):
        return Resource.objects.all()


class AddPersonView(CreateView):
    """Adds a new person"""
    # uses template person_form.html
    model = Person
    fields = ['first_name', 'last_name', 'cost']
    success_url = '/planer/list/person/'


class PersonListView(ListView):

    def get_queryset(self):
        return Person.objects.all()


class AddPersonBookingView(CreateView):
    """Books a person"""
    # uses template booking_form.html
    model = Booking
    fields = ['title', 'description', 'start_date', 'end_date', 'person']
    success_url = '/planer/booking/list/recent'


class AddResourceBookingView(CreateView):
    """Books a resource"""
    # uses template booking_form.html
    model = Booking
    fields = ['title', 'description', 'start_date', 'end_date', 'resource']
    success_url = '/planer/booking/list/recent'


class BookingListAllView(ListView):

    def get_queryset(self):
        # shows all bookings:
        return Booking.objects.all()


class BookingListRecentView(ListView):

    def get_queryset(self):
        # excludes all booking with an enddate before today
        return Booking.objects.all().exclude(end_date__lte=datetime.datetime.now())
