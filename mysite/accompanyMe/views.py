from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.contrib.sessions import serializers
from django.core.serializers import serialize
from django.forms import RadioSelect
from django.http import HttpResponse, JsonResponse
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
import pyqrcode
from django.views.generic import FormView
from .models import User, Ride, BookedRide, MyUser
from django.conf import settings
import datetime


# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# and use the E.164 format, for example: "+12025551234"
def audio(request):
    import speech_recognition as sr
    from pydub import AudioSegment
    from pydub.playback import play

    r = sr.Recognizer()
    dis = sr.Recognizer()
    time = sr.Recognizer()
    yesno = sr.Recognizer()

    while (True):
        song = AudioSegment.from_wav("destination.wav")
        play(song)
        with sr.Microphone() as source:
            print("SAY destination")
            audio = r.listen(source)
            print("over destination")
        try:
            dis = r.recognize_google(audio)
            print("TEXT destination: " + dis)
            break
        except:
            pass

    # while (True):
    #     song = AudioSegment.from_wav("time.wav")
    #     play(song)
    #     with sr.Microphone() as source:
    #         print("SAY time");
    #         audio = r.listen(source)
    #         print("over time")
    #     try:
    #         time = r.recognize_google(audio)
    #         print("TEXT time: " + time)
    #         break
    #     except:
    #         pass

    qs = Ride.objects.filter(destination=dis)  # , hour = time)
    if not qs:
        print("not found!!!!!!")
    else:
        print(" found!!!!!!")
        return render(request, "accompanyMe/view_rides.html", {
            'object_list': qs, })

    # while (True):
    #     song = AudioSegment.from_wav("not found.wav")
    #     play(song)
    #     with sr.Microphone() as source:
    #         print("SAY yes/no");
    #         audio = r.listen(source)
    #         print("over yes/no")
    #     try:
    #         yesno = r.recognize_google(audio)
    #         print("TEXT yes/no: " + yesno)
    #         break
    #     except:
    #         pass

    # import speech_recognition as spreg
    #
    # from pydub import AudioSegment
    # from pydub.playback import play
    #
    # sample_rate = 48000
    # data_size = 512
    #
    # song = AudioSegment.from_wav("destination.wav")
    # play(song)
    #
    # recog = spreg.Recognizer()
    # with spreg.Microphone(sample_rate=sample_rate, chunk_size=data_size) as source:
    #     recog.adjust_for_ambient_noise(source)
    #     print('Tell Something: ')
    #     speech = recog.listen(source)
    # try:
    #     text = recog.recognize_google(speech)  # Tel Aviv
    #     print('You have said: ' + text)
    #     # for ride in BookedRide:
    #     #     if(Ride.object.filter(destination = text)):
    #     #         print("find the destination!!")
    #     song = AudioSegment.from_wav("time.wav")
    #     play(song)
    #     speech1 = recog.listen(source)
    #     text = recog.recognize_google(speech1)  # 16:00
    #     # for ride in BookedRide:
    #     #     if(Ride.object.filter(destination = text) and Ride.object.filter(hour = text)):
    #     #         print("find the time!!")
    #     song = AudioSegment.from_wav("not found.wav")
    #     play(song)
    #     speech2 = recog.listen(source)
    #     text = recog.recognize_google(speech2)  # yes/no
    #
    # except spreg.UnknownValueError:
    #     print('Unable to recognize the audio')
    #
    # except spreg.RequestError as e:
    #     print("Request error from Google Speech Recognition service; {}".format(e))


def dial_numbers(numbers_list, msg):
    """Dials one or more phone numbers from a Twilio phone number."""
    # list of one or more phone numbers to dial, in "+19732644210" format
    for number in numbers_list:
        print("Dialing", number)
        settings.CLIENT.messages.create(
            body=msg,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=number
        )


# def index(request):
#     return render(request, "accompanyMe/index.html")


# ====================lists======================

def user_list(request):
    return render(request, "accompanyMe/user_list.html", {
        'object_list': User.objects.order_by("-username"),
    })


# def chunks(data, size):
#     cur = []
#     for x in data:
#         cur.append(x)
#         if len(cur) == size:
#             yield cur
#             cur = []
#     if cur:
#         yield cur


def ride_list(request):
    curr_date = datetime.date.today()
    qs = Ride.objects.all().filter(num_of_available_places__gt=0, date=curr_date).order_by('date').order_by('hour')
    # return render(request, "accompanyMe/view_rides.html", {
    #     'chunks': chunks(qs, 4),
    # })
    return render(request, "accompanyMe/view_rides.html", {
        'object_list': qs,
    })


def booked_ride_list(request):
    return render(request, "accompanyMe/view_bookedRides.html", {
        'object_list': BookedRide.objects.order_by("-ride_id"),
    })


# =================adding to dbs======================

class NewUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    phonenumber = forms.CharField(max_length=100)


def update(request):
    ret = Ride.objects.all()
    ret = serialize("json", ret)
    return HttpResponse(ret)
    # data = serialize('json', Ride.objects.all())
    # jobmstquery = Ride.objects()
    # return HttpResponse(data, content_type="application/json")
    # return JsonResponse({'latest_results_list': Ride.objects.all()})


class NewUserView(FormView):
    form_class = NewUserForm
    template_name = "accompanyMe/add_user.html"

    def form_valid(self, form):
        e = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        e1 = MyUser(
            user_id=e.id,
            phonenumber=form.cleaned_data["phonenumber"],
        )
        e1.save()
        messages.success(self.request, "")
        return redirect("accompanyMe:add_user")


class NewRideForm(forms.Form):
    destination = forms.CharField()
    hour = forms.TimeField()
    date = forms.DateField()
    num_of_available_places = forms.IntegerField()


class NewRideView(FormView):
    form_class = NewRideForm
    template_name = "accompanyMe/add_ride.html"

    def form_valid(self, form):
        e = Ride(
            driver=self.request.user,
            destination=form.cleaned_data["destination"],
            hour=form.cleaned_data["hour"],
            date=form.cleaned_data["date"],
            num_of_available_places=form.cleaned_data["num_of_available_places"],
        )
        e.save()
        messages.success(self.request, "")
        return redirect("accompanyMe:add_ride")


# def addride(request):
#     return render(request, "accompanyMe/add_ride.html")


# def add_a_ride(request):
#     e = Ride(
#         driver=request.user,
#         destination=request.POST["destination"],
#         hour=request.POST["hour"],
#         date=request.POST["date"],
#         num_of_available_places=request.POST["num_of_available_places"],
#     )
#     e.save()
#     return render(request, "accompanyMe/status.html", {'msg': "ride added successfuly", })
#     # return HttpResponse("ride added successfuly")


# ================details=====================
@login_required
def ride_detail(request, pk):
    o = get_object_or_404(Ride, pk=pk)
    # user = get_object_or_404(User, email=request.user.email)
    if o.num_of_available_places == 0:
        return render(request, "accompanyMe/status.html", {'msg': "ride is full!", })
        # return HttpResponse("ride is full!!!")
    o.num_of_available_places = o.num_of_available_places - 1
    o.save()
    e = BookedRide(
        ride_id=o,
        # user_email=request.user.email
        user=request.user
    )
    e.save()
    user = get_object_or_404(User, email=request.user.email)
    number = user.myuser.phonenumber
    print("Dialing:", number)
    dial_numbers([number], f"your ride to {o.destination} has been confirmed")
    return render(request, "accompanyMe/status.html", {'msg': "ride selected successfuly", })


def bar_code(request, pk):
    qr = pyqrcode.create(f"{settings.PUBLIC_URL}/{pk}")
    qr.png(f"{pk}.png", scale=6)
    image_data = open(f"{pk}.png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
    # qr = pyqrcode.create(f"{settings.PUBLIC_URL}/{pk}")
    # qr.png(f"{pk}.png", scale=6)
    # image_data = open(f"{pk}.png", "rb").read()
    # return HttpResponse(image_data, content_type="image/png")


# def remove(request):
#     # user_name = ["ron", 'messy', 'omry', 'israel']
#     #     # email = ["ron@gmail.com", 'messy@gmail.com', 'omry@gmail.com', 'israel@gmail.com']
#     #     # passw = ['ronron123', 'messymessy123', 'omryomry123', 'israelisrael123']
#     #     # phone = ['0583211223', '0583168008', '0556801421', '0556801421']
#     #     # for i, user in enumerate(user_name):
#     #     #     e = User.objects.create_user(
#     #     #         username=user,
#     #     #         email=email[i],
#     #     #         password=passw[i]
#     #     #     )
#     #     #     e1 = MyUser(
#     #     #         user_id=e.id,
#     #     #         phonenumber=phone[i],
#     #     #     )
#     #     #     e1.save()
#     return HttpResponse("remove")


def cancel(request):
    o = Ride.objects.filter(driver=request.user).distinct()
    return render(request, "accompanyMe/cancel_form.html", {'objects': o, })


def cancel_ride(request):
    qs = BookedRide.objects.filter(ride_id__id=request.POST.get('ride')).distinct()
    phones = [o.user.myuser.phonenumber for o in qs]
    dial_numbers(phones, f"your ride to {{ride_id_destination}} has been canceled")
    o = get_object_or_404(Ride, pk=request.POST.get('ride'))
    o.delete()
    return render(request, "accompanyMe/status.html", {'msg': "canceled successfully", })


def user_cancel(request):
    qs = BookedRide.objects.filter(user=request.user).distinct()
    return render(request, "accompanyMe/user_cancel_form.html", {'objects': qs, })


def user_cancel_ride(request):
    qs = Ride.objects.filter(id=request.POST.get('user_ride')).distinct()
    print("qs", qs)
    for o in qs:
        o.num_of_available_places = o.num_of_available_places + 1
        print("o", o)

    obj = BookedRide.objects.filter(user=request.user, ride_id_id=request.POST.get('user_ride'))
    print("obj", obj)
    obj.delete()
    return render(request, "accompanyMe/status.html", {'msg': "user ride canceled successfully", })
