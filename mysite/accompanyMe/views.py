from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
import pyqrcode

# from  models import Expense
from .models import User, Driver, Ride,BookedRide

def index(request):
    return render(request, "accompanyMe/index.html")


def user_list(request):
    return render(request, "accompanyMe/user_list.html", {
        'object_list': User.objects.order_by("-username"),
    })

def ride_list(request):
    return render(request, "accompanyMe/view_rides.html", {
        'object_list': Ride.objects.order_by("-hour"),
    })


def adduser(request):
    return render(request, "accompanyMe/add_user.html")


def add_a_user(request):  # ,name,email,phone
    e = User(
        # id=request.POST["id"],
        username=request.POST["name"],
        email=request.POST["emailAddress"],
        password=request.POST["password"]
        # phone_number=request.POST["phone"]
    )
    e.save()
    return HttpResponse("user added successfuly")


def adddriver(request):
    return render(request, "accompanyMe/add_driver.html")

def add_a_driver(request):  # ,name,email,phone
    e = Driver(
        # user_email = request.POST["useremail"],
        user_id=request.POST["id"],
        carsize=request.POST["carsize"],
        # destination = request.POST["destination"],
    )
    e.save()
    return HttpResponse("driver added successfuly")

def addride(request):
    return render(request, "accompanyMe/add_ride.html")

def add_a_ride(request):
    e = Ride(
        driver_email = request.POST["driveremail"],
        destination = request.POST["destination"],
        hour = request.POST["hour"],
        date=request.POST["date"],
        num_of_available_places = request.POST["num_of_available_places"],
        available=request.POST["available"],
    )
    e.save()
    return HttpResponse("ride added successfuly")




def bar_code(request):
   qr = pyqrcode.create("https://repl.it/@ronnysherer/")
   qr.png("horn.png", scale=6)
   qr.show()
   response = HttpResponse(mimetype="image/png")
   qr.png.save(response, "PNG")

   return response
   # return HttpResponse("ok")


def remove(request):
    User.objects.all().delete()
    return HttpResponse("remove")

def select_ride(request):
    e = BookedRide(
        ride_id=request.POST["object"].id,
        user_email=request.POST["object"].user_email
    )
    e.save()
    return HttpResponse("ride selected successfuly")

# def add_user(request):  # ,name,email,phone
#     if request.method=="POST":
#          form=UserForm(request.POST)
#     else:
#         form = UserForm()
#     return render(request, "accompanyMe/add_usr.html",{"form":form})

class UserForm(forms.Form):
    name=forms.CharField(max_length=100)
    email =forms.EmailField()
    password=forms.PasswordInput()
