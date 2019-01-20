from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.shortcuts import render, get_object_or_404, redirect

# from  models import Expense
from .models import Driver


def index(request):
    return render(request, "accompanyMe/index.html")


def user_list(request):
    return render(request, "accompanyMe/user_list.html", {
        'object_list': User.objects.order_by("-name"),
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


def add_a_driver(request):  # ,name,email,phone
    e = Driver(
        # user_email = request.POST["useremail"],
        user_id=request.POST["id"],
        carsize=request.POST["carsize"],
        # destination = request.POST["destination"],
    )
    e.save()
    return HttpResponse("driver added successfuly")


def adddriver(request):
    return render(request, "accompanyMe/add_driver.html")


def remove(request):
    User.objects.all().delete()
    return HttpResponse("remove")




#
# class ContactUsForm(forms.Form):
#     name=forms.CharField(max_length=300)
#     email=forms.TextField()
#     phone_number=forms.IntegerField()
#
# class ExpenseForm(forms.ModelForm):
#     class Meta:
#         model = Expense
#         fields = "__all__"
#
#
# def expense_create(request):
#     if request.method == "POST":
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("expenses:list")
#     else:
#         form = ExpenseForm()
#     return render(request, "accompanyMe/user_form.html", {
#         'form': form,
#     })
