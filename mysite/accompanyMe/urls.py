from django.urls import path

from . import views

app_name = "accompanyMe"

urlpatterns = [
    path('', views.expense_list, name="list"),
    path('add', views.add, name="add"),
    path('AddUser', views.add_a_user, name='add_a_user'),
    path('remove', views.remove, name="remove"),
    path('<int:pk>/',
         views.expense_detail,
         name="detail"),
]
