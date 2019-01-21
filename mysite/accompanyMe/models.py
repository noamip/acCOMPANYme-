from django.contrib.auth.models import User
from django.db import models
from django.forms import forms
from django.urls import reverse


class MyUser(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.IntegerField()


# request.user.driver


class Ride(models.Model):
    # user_id=models.IntegerField(primary_key=True)
    # driver_email = models.EmailField()
    driver=models.ForeignKey(User,on_delete=models.CASCADE)
    destination = models.TextField()
    hour = models.TimeField()
    date = models.DateField()
    num_of_available_places = models.IntegerField()

    # available = models.BooleanField()

    def get_absolute_url(self):
        return reverse("expenses:detail", args=(self.id,))

    def __str__(self):
        return f"[#{self.id}] {self.destination} {self.driver} {self.hour} {self.num_of_available_places} "


class BookedRide(models.Model):
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #
    # class Meta:
    #     unique_together = ( ('ride_id', 'user_email'),)
