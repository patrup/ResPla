import datetime
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.db.models import Q
from django import forms
from Planer.models import Resource, Booking, Person

from django.shortcuts import render


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


def get_available_resources(start_date, end_date):
    q1 = Q(booking__start_date__range=(start_date, end_date))
    q2 = Q(booking__end_date__range=(start_date, end_date))
    qset = get_available_resources_inside_span(start_date, end_date)
    return qset.all().exclude(q1 | q2)


def get_available_resources_inside_span(start_date, end_date):
    '''Gets all available resources with start_date and end_date
    in booking time span'''
    q1 = Q(booking__start_date__lt=start_date)
    q2 = Q(booking__end_date__gt=end_date)
    return Resource.objects.all().exclude(q1 & q2)


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


class PersonsTimeSpanForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    persons = forms.ModelChoiceField(queryset=Person.objects.all(),
                                     required=False)


class ResourceTimeSpanForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    resources = forms.ModelChoiceField(queryset=Resource.objects.all(),
                                       required=False)


def book_a_person(request):
    ''' books an available person '''
    if request.method == 'GET':
        person_list = Person.objects.all()
        form = PersonsTimeSpanForm()
        context = {'person_list': person_list, 'form': form}
        return render(request, 'Planer/book_person.html', context)
    if request.method == 'POST':
        form = PersonsTimeSpanForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['persons'] is not None:
                person = form.cleaned_data['persons']
                booking = Booking()
                booking.person = person
                booking.start_date = form.cleaned_data['start_date']
                booking.end_date = form.cleaned_data['end_date']
                booking.title = person.first_name + ' ' + person.last_name
                booking.description = "Personenbuchung"
                booking.save()
                return render(request, 'Planer/index.html')
            else:
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                person_list = get_available_persons(start_date, end_date)
                form.fields['persons'].queryset = person_list
        else:
            person_list = Person.objects.all()
        context = {'person_list': person_list, 'form': form}
        return render(request, 'Planer/book_person.html', context)


def book_a_resource(request):
    ''' books an available resource '''
    if request.method == 'GET':
        resource_list = Resource.objects.all()
        form = ResourceTimeSpanForm()
        context = {'resource_list': resource_list, 'form': form}
        return render(request, 'Planer/book_resource.html', context)
    if request.method == 'POST':
        form = ResourceTimeSpanForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['resources'] is not None:
                resource = form.cleaned_data['resources']
                booking = Booking()
                booking.resource = resource
                booking.start_date = form.cleaned_data['start_date']
                booking.end_date = form.cleaned_data['end_date']
                booking.title = resource.title
                booking.description = "Resourcenbuchung"
                booking.save()
                return render(request, 'Planer/index.html')
            else:
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                resource_list = get_available_resources(start_date, end_date)
                form.fields['resources'].queryset = resource_list
        else:
            resource_list = Resource.objects.all()
        context = {'resource_list': resource_list, 'form': form}
        return render(request, 'Planer/book_resource.html', context)