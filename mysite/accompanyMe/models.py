from django.db import models


# ORM: Object-Relational Mapper
class User(models.Model):
    # user_id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=300)
    email=models.TextField()
    phone_number=models.IntegerField()

    class Meta:
        unique_together = ["name", "email", "phone_number"]


    def __str__(self):
        return f"[#{self.id}] {self.name} @{self.email} @{self.phone_number}"

    # def is_expensive(self):
    #     return self.amount > 1000

