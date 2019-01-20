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
