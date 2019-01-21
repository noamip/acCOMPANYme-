from django.contrib.auth.models import User
from django.forms import RadioSelect
from django.http import HttpResponse
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
import pyqrcode
from .models import User, Ride, BookedRide, MyUser
from django.conf import settings

import client as client
from twilio.rest import Client


# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# and use the E.164 format, for example: "+12025551234"


def dial_numbers(numbers_list,msg):
    """Dials one or more phone numbers from a Twilio phone number."""
    # list of one or more phone numbers to dial, in "+19732644210" format
    for number in numbers_to_message:
        settings.CLIENT.messages.create(
            body=msg,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=number
        )


def index(request):
    # user = authenticate(username='sara', email='sjofen94@gmail.com')
    # if user is not None:
    #     return HttpResponse("ok")
    # else:
    #     return HttpResponse("not ok")
    return render(request, "accompanyMe/index.html")


# ====================lists======================

def user_list(request):
    return render(request, "accompanyMe/user_list.html", {
        'object_list': User.objects.order_by("-username"),
    })


def ride_list(request):
    return render(request, "accompanyMe/view_rides.html", {
        'object_list': Ride.objects.all().filter(num_of_available_places__gt=0).order_by('date').order_by('hour'),
    })


def booked_ride_list(request):
    return render(request, "accompanyMe/view_bookedRides.html", {
        'object_list': BookedRide.objects.order_by("-ride_id"),
    })


# =================adding to dbs======================
def adduser(request):
    return render(request, "accompanyMe/add_user.html")


def add_a_user(request):  # ,name,email,phone
    e = User(
        username=request.POST["name"],
        email=request.POST["emailAddress"],
        password=request.POST["password"]
        # phone_number=request.POST["phone"]
    )
    e.save()
    e1 = MyUser(
        user_id=e.id,
        phonenumber=request.POST["phonenumber"],
    )
    e1.save()

    return render(request, "accompanyMe/status.html", {'msg': "user added successfuly", })
    # return HttpResponse("user added successfuly")


def adddriver(request):
    return render(request, "accompanyMe/add_driver.html")


def add_a_driver(request):  # ,name,email,phone
    e = MyUser(
        user_id=request.POST["id"],
        phonenumber=request.POST["phonenumber"],
    )
    e.save()
    return render(request, "accompanyMe/status.html", {'msg': "driver added successfuly", })
    # return HttpResponse("driver added successfuly")


def addride(request):
    return render(request, "accompanyMe/add_ride.html")


def add_a_ride(request):
    e = Ride(
        driver_email=request.POST["driveremail"],
        destination=request.POST["destination"],
        hour=request.POST["hour"],
        date=request.POST["date"],
        num_of_available_places=request.POST["num_of_available_places"],
    )
    e.save()
    return render(request, "accompanyMe/status.html", {'msg': "ride added successfuly", })
    # return HttpResponse("ride added successfuly")


# ================details=====================
def ride_detail(request, pk):
    o = get_object_or_404(Ride, pk=pk)
    user = get_object_or_404(User, email=request.user.email)
    if o.num_of_available_places == 0:
        return render(request, "accompanyMe/status.html", {'msg': "ride is full!", })
        # return HttpResponse("ride is full!!!")
    o.num_of_available_places = o.num_of_available_places - 1
    o.save()
    e = BookedRide(
        ride_id=o,
        user_email="noamijofen@gmail.com"
    )
    e.save()
    return render(request, "accompanyMe/status.html", {'msg': "ride selected successfuly", })
    # return HttpResponse("ride selected successfuly")


def bar_code(request, pk):
    # url = reverse("my_view_name", args=(pk,))
    # full_url = settings.PUBLIC_URL + url
    # qr = pyqrcode.create(full_url)
    qr = pyqrcode.create(f"{ settings.PUBLIC_URL}/{pk}")
    qr.png(f"{pk}.png", scale=6)
    image_data = open(f"{pk}.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def remove(request):
    BookedRide.objects.all().delete()
    return HttpResponse("remove")


def cancel(request):
    o = Ride.objects.filter(driver_email=request.user.email).distinct()
    return render(request, "accompanyMe/cancel_form.html", {'objects': o, })


def cancel_ride(request):
    # assert False, (request.POST.get('ride'), request.user)
    o = get_object_or_404(Ride, pk=request.POST.get('ride'))
    o.delete()
    users = BookedRide.objects.filter(ride_id__id=request.POST.get('ride')).valuelist('user_email').distinct()
    user_phone=[user.MyUser.phonenumber for user in users]
    dial_numbers(user_phone,f"your ride to {{ride_id_destination}} has been canceled")
    return render(request, "accompanyMe/status.html", {'msg': "canceled successfully", })


# ================forms==================
# class CancelForm(forms.Form):
#     o = BookedRide.objects.all().filter(user_email="noamijofen@gmail.com")
#     rides = forms.ChoiceField(widget=RadioSelect(), choices=[(j, obj.ride_id.id) for j, obj in enumerate(o)])


class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.PasswordInput()
