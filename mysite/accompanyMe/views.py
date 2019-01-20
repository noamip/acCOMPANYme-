from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
import pyqrcode

# from  models import Expense
from .models import User

def expense_list(request):
    return render(request, "accompanyMe/user_list.html", {
        'object_list': User.objects.order_by("-name"),
    })

def add_a_user(request):#,name,email,phone
    e = User(
        name=request.POST["name"],
        email=request.POST["emailAddress"],
        phone_number=request.POST["phone"]
    )
    e.save()
    return HttpResponse("good")



def add(request):
    return render(request, "accompanyMe/add_user.html" )


def bar_code(request):
    url = pyqrcode.create('http://uca.edu')
    url.svg('uca-url.svg', scale=8)
    url.eps('uca-url.eps', scale=2)
    print(url.terminal(quiet_zone=1))
    return render(request, "accompanyMe/add_user.html")


def remove(request):
    User.objects.all().delete()
    return HttpResponse("remove")


def expense_detail(request, pk):
    o = get_object_or_404(User, pk=pk)

    return render(request, "accompanyMe/user_detail.html", {
        'object': o,
    })


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

