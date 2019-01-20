from django.contrib.auth.models import User
from django.db import models
from django.forms import forms


class Driver(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    carsize = models.IntegerField()

 # user_email = models.EmailField()

# destination = models.TextField()


class Ride(models.Model):
    # user_id=models.IntegerField(primary_key=True)
    driver_email = models.EmailField()
    destination = models.TextField()
    hour = models.TimeField()
    date = models.DateField()
    num_of_available_places = models.IntegerField()
    available = models.BooleanField()

    def __str__(self):
        return f"[#{self.id}] {self.destination} {self.driver_email} {self.hour} {self.num_of_available_places} @{self.available}"



class BookedRide(models.Model):
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE)
    # user_email = models.EmailField()
    user_email = models.ForeignKey(User, on_delete=models.CASCADE)



    # def __str__(self):
    #     return f"[ #{self.id}] {self.destination} {self.driver_email} {self.hour} {self.num_of_available_places}"

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = "__all__"
