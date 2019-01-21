from django.urls import path

from django.conf import settings
from . import views


app_name = "accompanyMe"

urlpatterns = [
    path('', views.ride_list, name="ride_list"),
    path('index', views.index, name="index"),
    path('list', views.user_list, name="list"),
    # path('Rides', views.ride_list, name="ride_list"),
    path('BRides', views.booked_ride_list, name="booked_ride_list"),

    path('add_user', views.adduser, name="adduser"),
    # path('add_driver', views.adddriver, name="adddriver"),
    path('add_ride', views.addride, name="add_ride"),
    path('AddUser', views.add_a_user, name='add_a_user'),

    path('add_ride', views.addride, name="addride"),
    path('AddRide', views.add_a_ride, name='add_a_ride'),

    path('remove', views.remove, name="remove"),
    # path('ride/<int:pk>', views.ride_detail,name="ride detail"),
    path('BarCode/<int:pk>', views.bar_code, name="bar_code"),

    path('<int:pk>/', views.ride_detail, name="detail"),
    path('BRides', views.booked_ride_list, name="booked_ride_list"),
    path(f'<int:pk>/', views.ride_detail, name="detail"),
    path('Cancel', views.cancel, name="Cancel"),
    path('CancelRide', views.cancel_ride, name="cancel_ride"),
# path('selectRide', views.select_ride, name="select_ride"),
]



