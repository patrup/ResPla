from django.test import TestCase
from datetime import datetime

from Planer.models import Person
from Planer.views import get_available_persons


class ListAvailablePersonsTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        Person.objects.create(first_name="Franz",
                              last_name="Alberts", cost=20.12)
        Person.objects.create(first_name="Peter",
                              last_name="Phillips", cost=19.12)
        Person.objects.create(first_name="Availy",
                              last_name="Nevers", cost=34.07)

    def test_db_is_not_empty(self):
        qs = Person.objects.all()
        self.assertGreater(qs.count(), 0, "DB is empty!")

    def test_three_are_available(self):
        start_date = datetime(2014, 10, 1)
        end_date = datetime(2014, 10, 3)
        qs = get_available_persons(start_date, end_date)
        count = qs.count()
        self.assertEqual(count, 3, "Should be three entries!")
