from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import IntegerField
# Create your models here.
class Referrals(models.Model):
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    referral_code = models.TextField()
    email = models.TextField()


    def __str__(self):
        return self.university

class UserData(models.Model):
    username = models.CharField(max_length=200)
    api_key = models.TextField(max_length=500)
    referral_code = models.TextField(max_length=30)

    def __str__(self):
        return self.username


class Events(models.Model):
    referral_code = models.TextField()
    event_code = models.TextField()
    certificate_default_content = models.TextField(max_length=500)
    template_number = models.IntegerField()
    event_name = models.TextField()


class Event_Certificates(models.Model):
    event_code = models.TextField()
    uid_number = models.TextField()


class Certificates(models.Model):
    uid_number = models.TextField()
    event_code = models.TextField()
    participant_id = models.TextField()
    participant_name = models.TextField()
    certificate_link = models.TextField()


    

