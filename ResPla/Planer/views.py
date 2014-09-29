import datetime
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic import ListView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django.db.models import Q
from django import forms
from django.core.urlresolvers import reverse
from Planer.models import Resource, Booking, Person
from django.views.generic.base import TemplateResponseMixin


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


class TimeSpanForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


class ShowAvailablePersonsView(FormView):
    template_name = 'Planer/book_person.html'
    form_class = TimeSpanForm

    def get_queryset(self):
        if len(self.kwargs) == 0:
            return Person.objects.all()
        else:
            sd = '2014-10-07'
            ed = '2014-10-13'
            return get_available_persons(sd, ed)

    def get_context_data(self, **kwargs):
        return FormView.get_context_data(self, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(ShowAvailablePersonsView, self).get(request,
                                                         *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(ShowAvailablePersonsView, self).post(request,
                                                          *args, **kwargs)


class CreateBookingListView(ListView, FormMixin):
    template_name = 'Planer/book_person.html'
    form_class = TimeSpanForm

    def __init__(self):
        self.sd = None
        self.ed = None

    def form_invalid(self, form):
        return FormMixin.form_invalid(self, form)

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
        # return FormMixin.form_invalid(self, form)
        # return FormMixin.form_valid(self, form)

    def get_queryset(self):
        if self.sd is None:
            return Person.objects.all()
        else:
            # sd = '2014-10-07'
            # ed = '2014-10-13'
            return get_available_persons(self.sd, self.ed)

    def get_context_data(self, **kwargs):
        context = super(CreateBookingListView, self).get_context_data(**kwargs)
        context['form'] = TimeSpanForm()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.sd = request.POST['start_date']
            self.ed = request.POST['end_date']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        # return super(CreateBookingListView, self).get(request, *args, **kwargs)


class CreateBookingFormView(MultipleObjectMixin, CreateView):
    template_name = 'Planer/book_person.html'
    # form_class = TimeSpanForm
    model = Booking
    fields = ['start_date', 'end_date']

    def get_queryset(self):
        return Person.objects.all()

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        sd = request.POST['start_date']
        return super(CreateBookingFormView, self).post(request,
                                                       *args, **kwargs)


class CreateBookingView(View):

    def get(self, request, *args, **kwargs):
        view = CreateBookingListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateBookingListView.as_view()
        return view(request, *args, **kwargs)


class BookAPersonView(MultipleObjectMixin, TemplateResponseMixin, View):
    template_name = 'Planer/book_person.html'
    form_class = TimeSpanForm

    def get_context_data(self, **kwargs):
        context = super(CreateBookingListView, self).get_context_data(**kwargs)
        context['form'] = TimeSpanForm()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        view = CreateBookingListView.as_view()
        return view(request, *args, **kwargs)
