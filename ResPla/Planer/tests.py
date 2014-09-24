from django.test import TestCase
from datetime import datetime

from Planer.models import Person, Booking
from Planer.views import get_available_persons


class ListAvailablePersonsTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        franz = Person.objects.create(first_name="Franz",
                                      last_name="Alberts", cost=20.12)
        Person.objects.create(first_name="Peter",
                              last_name="Phillips", cost=19.12)
        Person.objects.create(first_name="Tom",
                              last_name="Nevers", cost=34.07)
        Booking.objects.create(title="One",
                               description="The only One.",
                               start_date=datetime(2014, 10, 2),
                               end_date=datetime(2014, 10, 5),
                               person=franz)

    def test_db_is_not_empty(self):
        qs = Person.objects.all()
        self.assertGreater(qs.count(), 0, "No Persons!")

    def test_start_date_before_and_end_date_in_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 3)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")

    def test_start_date_in_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 10)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")

    def test_start_date_in_and_end_date_in_timespan(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 4)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")
