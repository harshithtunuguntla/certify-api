
from os import name
from django.urls import path

from . import views


urlpatterns = [
    path('verifycertificate',views.verifycertificate_view,name="verify_certificate"),
    path('fetchcertificate',views.fetchcertificate_view,name="fetch_certificate"),
    path('verifyuser',views.verifyuser_view,name="verifyuser"),
    path('usersignup',views.usersignup_view,name="usersignup"),

    ]