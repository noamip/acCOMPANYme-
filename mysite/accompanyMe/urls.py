from django.urls import path

from . import views

app_name = "accompanyMe"

urlpatterns = [
    path('', views.expense_list, name="list"),
    path('add_user', views.adduser, name="adduser"),
    path('add_driver', views.adddriver, name="adddriver"),
    path('AddUser', views.add_a_user, name='add_a_user'),
    path('AddDriver', views.add_a_driver, name='add_a_driver'),
    path('remove', views.remove, name="remove"),
    path('<int:pk>/',
         views.expense_detail,
         name="detail"),
]
