from django.contrib import admin
from .models import Referrals, UserData, Certificates, Event_Certificates, Events
# Register your models here.


admin.site.register(Referrals)
admin.site.register(UserData)
admin.site.register(Certificates)
admin.site.register(Event_Certificates)
admin.site.register(Events)

