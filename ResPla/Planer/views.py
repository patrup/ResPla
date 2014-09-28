import datetime
from django.views.generic.edit import CreateView
from django.views.generic import ListView, FormView, View
from django.views.generic.detail import SingleObjectMixin

from django.db.models import Q
from django import forms
from django.core.urlresolvers import reverse
from Planer.models import Resource, Booking, Person


def get_available_persons(start_date, end_date):
    q1 = Q(booking__start_date__range=(start_date, end_date))
    q2 = Q(booking__end_date__range=(start_date, end_date))
    qset = get_available_persons_inside_span(start_date, end_date)
    return qset.all().exclude(q1 | q2)


def get_available_persons_inside_span(start_date, end_date):
    '''Gets all available persons with start_date and end_date
    in booking time span'''
    q1 = Q(booking__start_date__lt=start_date)
    q2 = Q(booking__end_date__gt=end_date)
    return Person.objects.all().exclude(q1 & q2)


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


class AvailableResourceListView(ListView):

    def get_queryset(self):
        return Resource.objects.all().filter(booking__start_date='2014-10-01')


class AddPersonView(CreateView):
    """Adds a new person"""
    # uses template person_form.html
    model = Person
    fields = ['first_name', 'last_name', 'cost']
    success_url = '/planer/list/person/'


class PersonListView(ListView):

    def get_queryset(self):
        return Person.objects.all()


class AvailablePersonListView(ListView):

    def get_queryset(self):
        sd = '2014-10-01'
        ed = '2014-10-03'
        return get_available_persons(sd, ed)


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


class BookResourceView(CreateView):
    """Books a resource if available"""
    # uses template booking_form.html
    model = Booking
    fields = ['title', 'description', 'start_date', 'end_date', 'resource']
    success_url = '/planer/booking/list/recent'

    def __init__(self, **kwargs):
        CreateView.__init__(self, **kwargs)
        # TODO: chatch the error
        # self.fields[4].queryset = Resource.objects.all().filter(title__contains='u')


class BookingListAllView(ListView):

    def get_queryset(self):
        # shows all bookings:
        return Booking.objects.all()


class BookingListRecentView(ListView):

    def get_queryset(self):
        # excludes all booking with an enddate before today
        return Booking.objects.all()\
            .exclude(end_date__lte=datetime.datetime.now())


class CreateTimeSpanView(ListView):
    model = Person
    template_name = 'Planer/book_person.html'

    def get_queryset(self):
        sd = '2014-10-07'
        ed = '2014-10-13'
        return get_available_persons(sd, ed)


class ShowAvailablePersonsView(ListView):

    def get_queryset(self):
        sd = '2014-10-07'
        ed = '2014-10-13'
        return get_available_persons(sd, ed)


class TimeSpanForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


class CreateBookingListView(ListView):
    template_name = 'Planer/book_person.html'

    def get_queryset(self):
        if len(self.kwargs) == 0:
            return Person.objects.all()
        else:
            sd = '2014-10-07'
            ed = '2014-10-13'
            return get_available_persons(sd, ed)

    def get_context_data(self, **kwargs):
        context = super(CreateBookingListView, self).get_context_data(**kwargs)
        context['form'] = TimeSpanForm()
        return context


class CreateBookingFormView(SingleObjectMixin, FormView):
    template_name = 'Planer/book_person.html'
    form_class = TimeSpanForm
    model = Booking

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CreateBookingFormView, self).post(request,
                                                       *args, **kwargs)


class CreateBookingView(View):

    def get(self, request, *args, **kwargs):
        view = CreateBookingListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateBookingFormView.as_view()
        return view(request, *args, **kwargs)
