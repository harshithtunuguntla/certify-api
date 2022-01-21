
from os import name
from django.urls import path

from . import views


urlpatterns = [
    path('verify/<int:verify_uid>',views.verifyuid,name="verifyuid"),
    ]