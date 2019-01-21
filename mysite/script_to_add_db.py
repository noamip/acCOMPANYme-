from django.contrib.auth.models import User

from mysite.accompanyMe.models import MyUser
from . import views

user_name = ["ron" , 'messy','omry','israel']
email = ["ron@gmail.com" , 'messy@gmail.com','omry@gmail.com','israel@gmail.com']
passw =['ronron123','messymessy123','omryomry123','israelisrael123']
phone = ['0583211223','0583168008','0556801421','0556801421']
def add_users():
    for i,user in enumerate(user_name):
        e = User.objects.create_user(
            username=user,
            email=email[i],
            password=passw[i]
        )
        e1 = MyUser(
            user_id=e.id,
            phonenumber=phone[i],
        )
        e1.save()

add_users()