from django.urls import path


from . import views

app_name = "ride"

urlpatterns = [
    path('', views.index, name="index"),
    path('list', views.user_list, name="list"),
    path('add_user', views.adduser, name="adduser"),
    path('add_driver', views.adddriver, name="adddriver"),
    path('add_ride', views.addride, name="addride"),
    path('AddUser', views.add_a_user, name='add_a_user'),
    path('AddDriver', views.add_a_driver, name='add_a_driver'),
    path('AddRide', views.add_a_ride, name='add_a_ride'),
    path('remove', views.remove, name="remove"),
    path('BarCode/', views.bar_code, name="bar_code"),
    path('Rides/', views.ride_list, name="ride_list"),
    path('selectRide', views.select_ride, name="select_ride"),
    path('<int:pk>/', views.ride_detail, name="detail"),
]
