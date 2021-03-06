# import pdb
from django.test import TestCase
from datetime import datetime

from Planer.models import Person, Booking, Resource
from Planer.views import get_available_persons, get_available_resources
from Planer.views import get_available_persons_inside_span
from Planer.views import get_available_resources_inside_span


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
        # pdb.set_trace()
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 4)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")

    def test_start_date_before_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 6)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")

    def test_start_date_before_and_end_date_before_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 1)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertTrue(franz_exists, "Franz should be available!")

    def test_start_date_after_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 6)
        end_date = datetime(2014, 10, 10)
        available_persons = get_available_persons(start_date, end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertTrue(franz_exists, "Franz should be available!")

    def test_available_persons_with_start_end_in_booking_span(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 4)
        available_persons = get_available_persons_inside_span(start_date,
                                                              end_date)
        franz_exists = available_persons.filter(first_name="Franz").exists()
        self.assertFalse(franz_exists, "Franz should not be available!")


class ListAvailableResoucesTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        itemA = Resource.objects.create(title="Item A", cost=20.12)
        Resource.objects.create(title="Item B", cost=19.12)
        Resource.objects.create(title="Item C", cost=34.07)
        Booking.objects.create(title="One",
                               description="The only One.",
                               start_date=datetime(2014, 10, 2),
                               end_date=datetime(2014, 10, 5),
                               resource=itemA)

    def test_db_is_not_empty(self):
        qs = Resource.objects.all()
        self.assertGreater(qs.count(), 0, "No Resources!")

    def test_start_date_before_and_end_date_in_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 3)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertFalse(itemA_exists, "Item A should not be available!")

    def test_start_date_in_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 10)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertFalse(itemA_exists, "Item A should not be available!")

    def test_start_date_in_and_end_date_in_timespan(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 4)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertFalse(itemA_exists, "Item A should not be available!")

    def test_start_date_before_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 6)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertFalse(itemA_exists, "Item A should not be available!")

    def test_start_date_before_and_end_date_before_timespan(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 1)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertTrue(itemA_exists, "Item A should be available!")

    def test_start_date_after_and_end_date_after_timespan(self):
        start_date = datetime(2014, 10, 6)
        end_date = datetime(2014, 10, 10)
        available_resources = get_available_resources(start_date, end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertTrue(itemA_exists, "Item A should be available!")

    def test_available_persons_with_start_end_in_booking_span(self):
        start_date = datetime(2014, 10, 3)
        end_date = datetime(2014, 10, 4)
        available_resources = get_available_resources_inside_span(start_date,
                                                                  end_date)
        itemA_exists = available_resources.filter(title="Item A").exists()
        self.assertFalse(itemA_exists, "Item A should not be available!")
