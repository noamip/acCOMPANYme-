from django.contrib.auth.models import User
from django.forms import RadioSelect
from django.http import HttpResponse
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
import pyqrcode
from .models import User, Driver, Ride, BookedRide
from .models import User, Ride, BookedRide
from django.conf import settings


# Driver


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
        'object_list': Ride.objects.order_by("-hour"),
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
    e1 = Driver(
        user_id=e,
        phonenumber=request.POST["phonenumber"],
    )
    e1.save()
    return HttpResponse("user added successfuly")


def adddriver(request):
    return render(request, "accompanyMe/add_driver.html")


def add_a_driver(request):  # ,name,email,phone
    e = Driver(
        user_id=request.POST["id"],
        phonenumber=request.POST["phonenumber"],
    )
    e.save()
    return HttpResponse("driver added successfuly")


def addride(request):
    return render(request, "accompanyMe/add_ride.html")


def add_a_ride(request):
    e = Ride(
        driver_email=request.POST["driveremail"],
        destination=request.POST["destination"],
        hour=request.POST["hour"],
        date=request.POST["date"],
        num_of_available_places=request.POST["num_of_available_places"],
        available=request.POST["available"],
    )
    e.save()
    return HttpResponse("ride added successfuly")


# ================details=====================
def ride_detail(request, pk):
    o = get_object_or_404(Ride, pk=pk)
    user = get_object_or_404(User, email="noamijofen@gmail.com")
    if o.num_of_available_places == 0:
        return HttpResponse("ride is full!!!")
    o.num_of_available_places = o.num_of_available_places - 1
    o.save()
    e = BookedRide(
        ride_id=o,
        user_email="noamijofen@gmail.com"
    )
    e.save()
    return HttpResponse("ride selected successfuly")


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
    o = BookedRide.objects.all().filter(user_email="noamijofen@gmail.com").values_list('ride_id').distinct()
    return render(request, "accompanyMe/cancel_form.html", {'objects': o, })


def cancel_ride(request):
    # o = get_object_or_404(Ride, pk=request.POST.get("id"))
    # o.delete()
    # return HttpResponse(request.POST)
    return HttpResponse("canceled")


# def cancel(request):
#     if request.method == "POST":
#         form = CancelForm(request.POST)
#         if form.is_valid():
#             o = get_object_or_404(Ride, pk=request.POST)
#             o.delete()
#         else:
#             form = CancelForm()
#             return render(request, "accompanyMe/cancel_form.html", {'form': form, })
#         return HttpResponse("canceled")
#     else:
#         form = CancelForm()
#     return render(request, "accompanyMe/cancel_form.html", {'form': form, })


# ================forms==================
class CancelForm(forms.Form):
    o = BookedRide.objects.all().filter(user_email="noamijofen@gmail.com")
    rides = forms.ChoiceField(widget=RadioSelect(), choices=[(j, obj.ride_id.id) for j, obj in enumerate(o)])


class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.PasswordInput()
