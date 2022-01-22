from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
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


