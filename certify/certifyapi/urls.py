
from os import name
from django.urls import path

from . import views


urlpatterns = [
    path('verifycertificate',views.verifycertificate_view,name="verify_certificate"),
    path('fetchcertificate',views.fetchcertificate_view,name="fetch_certificate"),
    path('verifyuser',views.verifyuser_view,name="verifyuser"),
    path('usersignup',views.usersignup_view,name="usersignup"),
    path('requestreferral',views.requestreferral_view,name="requestreferral"),
    path('showreferral',views.showreferral_view,name="showreferral"),
    path('showapi',views.showapi_view,name="showapi"),
    path('registerevent',views.registerevent_view,name="registerevent"),
    path('addcertificate',views.addcertificate_view,name="addcertificate"),
    path('getevents',views.getevents_view,name="getevents"),
    path('geteventcertificates',views.geteventcertificates_view,name="geteventcertificates"),


    path('emailcertificate',views.emailcertificate_view,name="emailcertificate"),







    ]