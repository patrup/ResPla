from django.db import models


class Resource(models.Model):
    title = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Booking(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date finished')
    resource = models.ForeignKey(Resource, null=True)
    person = models.ForeignKey(Person, null=True)

    def __str__(self):
        return self.title
