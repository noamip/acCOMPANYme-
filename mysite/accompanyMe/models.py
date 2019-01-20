from django.db import models


# ORM: Object-Relational Mapper
class User(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    phone_number = models.DecimalField(decimal_places=9, max_digits=9)

    def __str__(self):
        return f"[#{self.id}] {self.name} @{self.email} @{self.phone_number}"


class Driver(models.Model):
    # user_id=models.IntegerField(primary_key=True)
    user_email = models.EmailField()
    carsize = models.IntegerField()
    destination = models.TextField()

    def __str__(self):
        return f"[#{self.id}] {self.user_id} @{self.carsize} @{self.destination}"


class Ride(models.Model):
    # user_id=models.IntegerField(primary_key=True)
    driver_email = models.EmailField()
    destination = models.TextField()
    hour =  models.TimeField()
    date = models.DateField()
    num_of_available_places = models.IntegerField()
    available = models.BooleanField()

    def __str__(self):
        return f"[#{self.id}] {self.destination} {self.driver_email} {self.hour} {self.num_of_available_places} @{self.available}"
