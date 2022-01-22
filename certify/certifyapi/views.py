from importlib.resources import contents
from turtle import position
from django.http import HttpResponse
from django.shortcuts import render
import json
import secrets
from django.core import serializers

from django.contrib import auth


#Importing Databases
from certifyapi.models import Referrals, UserData, Event_Certificates, Events, Certificates
from django.contrib.auth.models import User


from django.core.mail import send_mail


#  Not Views
from . import testing_images



# Create your views here.

def verifycertificate_view(request):

    print("inside verifycertificate view")

    received_parameters = {}
    received_parameters['uid_number'] = request.GET.get('uid_number',None)


    if(received_parameters['uid_number']==None):
        error_message = {}
        error_message['message'] = "UID Number null"
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    if(Certificates.objects.filter(uid_number=received_parameters['uid_number']).exists()):
        certificateobj = Certificates.objects.filter(uid_number=received_parameters['uid_number'])
        
        success_message = {}
        success_message['Certificate Status'] = "Verified"
        success_message['Participant Name'] = certificateobj[0].participant_name
        success_message['Date Issued'] = certificateobj[0].date_issued
        success_message['Content'] = certificateobj[0].content
        success_message['Position'] = certificateobj[0].position

        # success_message['username'] = certificateobj
        return HttpResponse(json.dumps(success_message),content_type='application/json') 

    else:
        error_message = {}
        error_message['Certificate Status'] = 'Not Verified'
        error_message['Message'] = 'We cannot find the UID number you provided, please check again or contact issuer'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    #To-do
    #What format should I return that certificate is verified

    #Return Statement
    # verification_status = {}
    # verification_status['status'] = '200'
    # verification_status['response'] = 'OK'
    # verification_status['message'] = 'verified'

    # return HttpResponse(json.dumps(received_parameters),content_type='application/json')
    return HttpResponse("Data Received, no errors, database not added, will let you know if certificate is verified")


def fetchcertificate_view(request):

    print("inside fetchcertificate view")

    received_parameters = {}
    received_parameters['name'] = request.GET.get('name',None)
    received_parameters['university'] = request.GET.get('university',None)
    received_parameters['event_code'] = request.GET.get('event_code',None)
    received_parameters['participant_id'] = request.GET.get('participant_id',None)

    err= " "
    return_status=False
    if(received_parameters['event_code']==None):
        err += " [event code null] "
        return_status=True
    if(received_parameters['participant_id']==None):
        err += " [participant id null] "
        return_status=True


    if(return_status==True):
        error_message = {}
        error_message['message'] = err
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    
    if(Certificates.objects.filter(participant_id=received_parameters['participant_id'],event_code=received_parameters['event_code']).exists()):


        certificateobj = Certificates.objects.filter(participant_id=received_parameters['participant_id'],event_code=received_parameters['event_code'])

        success_message = {}
        success_message['Participant Name'] = certificateobj[0].participant_name
        success_message['Certificate Link'] = certificateobj[0].certificate_link
        success_message['UID'] = certificateobj[0].uid_number
        return HttpResponse(json.dumps(success_message),content_type='application/json') 

    else:
        error_message = {}
        error_message['message'] = 'Certificate Not found..Please check your details or contact issuer'
        return HttpResponse(json.dumps(error_message),content_type='application/json')


    # return HttpResponse(json.dumps(received_parameters),content_type='application/json') #Data Received

    #To-do
    #Add authentication headers
    #Add database
    #Verify against database
    #Return the Url feteched, Firebase Storage or Postgres

    return HttpResponse("Data Received, no errors, database not added, will let you know if certificate if found, will send data")


def verifyuser_view(request):

    print("Inside Verify User View")
    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    # login(username,password)
    # If username and password matched -> return sucess
    # Else return invalid credentials -> account not exists/they dont match

    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            success_message = {}
            success_message['message'] = 'User Succesfully Verified'
            return HttpResponse(json.dumps(success_message),content_type='application/json')
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')


    
def usersignup_view(request):
    print("inside user signup view")

    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    received_parameters = {}
    received_parameters['name'] = request.GET.get('name',None)
    received_parameters['referral_code'] = request.GET.get('referral_code',None)

    if Referrals.objects.filter(referral_code=received_parameters['referral_code']).exists():

        if User.objects.filter(username=username).exists():
            error_message = {}
            error_message['message'] = 'The username already exists, try another one'
            return HttpResponse(json.dumps(error_message),content_type='application/json')

        else:

            user = User.objects.create_user(username=username,password=password,first_name=received_parameters['name'])
            user.save()
            
            api_key = secrets.token_hex(16)


            while UserData.objects.filter(api_key=api_key).exists():
                api_key = secrets.token_hex(16)


            userdata = UserData.objects.create(api_key=api_key,referral_code=received_parameters['referral_code'],username=user.username)
            userdata.save()

            success_message = {}
            success_message['message'] = 'User Succesfully Created'
            return HttpResponse(json.dumps(success_message),content_type='application/json')

    else:
        error_message = {}
        error_message['message'] = 'The referral code doesnot exists, please provide valid one'
        return HttpResponse(json.dumps(error_message),content_type='application/json')



    #Do the logic to add user to an organisation based on referral code, if referral code not found do necessary things etx


    response_status = {}
    response_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(response_status),content_type="application/json")

def requestreferral_view(request):

    print("inside requestreferral view")

    received_parameters = {}
    received_parameters['name'] = request.GET.get('name',None)
    received_parameters['university'] = request.GET.get('university',None)
    received_parameters['email'] = request.GET.get('email',None)
    received_parameters['reason'] = request.GET.get('reason',None)

    new_referral_code = secrets.token_hex(8)
    while Referrals.objects.filter(referral_code=new_referral_code).exists():
        new_referral_code = secrets.token_hex(8)


    referral = Referrals.objects.create(name=received_parameters['name'],university=received_parameters['university'],email=received_parameters['email'],reason=received_parameters['reason'],referral_code=new_referral_code)
    referral.save()

    success_message = {}
    success_message['message'] = 'Your referral code is generated and is under pending state, we will get back to you once it is generated. This is a normal check to keep server from spamming. You will receive a mail if we found its legit.'
    success_message['referral_code'] = new_referral_code
    # send_mail(
    #     received_parameters['name'],
    #     'Your Referral Token has been succesfully genenerated' + new_referral_code,
    #     "harshithtunuguntla@gmail.com",
    #     received_parameters['email'],
    # )
    
    return HttpResponse(json.dumps(success_message),content_type='application/json')



def showreferral_view(request):

    print("Inside showreferral view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    
    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            userobj = UserData.objects.filter(username=username)     
            success_message = {}
            success_message['Referral Code'] = userobj[0].referral_code
            success_message['username'] = username
            return HttpResponse(json.dumps(success_message),content_type='application/json')       
            
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')


def showapi_view(request):

    print("Inside showapi view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    
    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            userobj = UserData.objects.filter(username=username)     
            success_message = {}
            success_message['API Key'] = userobj[0].api_key
            success_message['username'] = username
            return HttpResponse(json.dumps(success_message),content_type='application/json')       
            
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')



def registerevent_view(request):

    print("Inside addevent view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    


    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            received_parameters = {}
            received_parameters['event_name'] = request.GET.get('event_name',None)
            received_parameters['event_code'] = request.GET.get('event_code',None)
            received_parameters['certificate_default_content'] = request.GET.get('certificate_default_content',None)
            received_parameters['template_number'] = request.GET.get('template_number',None)

            err= " "
            return_status=False
            if(received_parameters['event_code']==None):
                err += " [event code null] "
                return_status=True
            if(received_parameters['event_name']==None):
                err += " [event name null] "
                return_status=True
            if(received_parameters['template_number']==None):
                err += " [template number null] "
                return_status=True
            if(received_parameters['certificate_default_content']==None):
                err += " [certificate default content null] "
                return_status=True


            if(return_status==True):
                error_message = {}
                error_message['message'] = err
                return HttpResponse(json.dumps(error_message),content_type='application/json')

            
            if Events.objects.filter(event_code=received_parameters['event_code']).exists():

                error_message = {}
                error_message['message'] = 'Event Code already exists, Please try with new event code'
                return HttpResponse(json.dumps(error_message),content_type='application/json')


            else:

                x = UserData.objects.filter(username=username)
                referral_code = x[0].referral_code
                # print(referral_code)

                Events.objects.create(referral_code=referral_code,event_code=received_parameters['event_code'],certificate_default_content=received_parameters['certificate_default_content'],template_number=received_parameters['template_number'],event_name=received_parameters['event_name'])

                success_message = {}
                success_message['message'] = 'User Succesfully Verified and Event Has been added'
                return HttpResponse(json.dumps(success_message),content_type='application/json')
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    
    # response_status = {}
    # response_status['message'] = 'Right now you are inside'

    # return HttpResponse(json.dumps(received_parameters),content_type="application/json")

def addcertificate_view(request):

    print("Inside addcertificate view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            received_parameters = {}
            received_parameters['event_code'] = request.GET.get('event_code',None)
            received_parameters['participant_name'] = request.GET.get('participant_name',None)
            received_parameters['participant_id'] = request.GET.get('participant_id',None)
            received_parameters['content'] = request.GET.get('content',None)
            received_parameters['position'] = request.GET.get('position',None)




            err= " "
            return_status=False
            if(received_parameters['event_code']==None):
                err += " [event code null] "
                return_status=True
            if(received_parameters['participant_name']==None):
                err += " [participant name null] "
                return_status=True
            if(received_parameters['participant_id']==None):
                err += " [participant id null] "
                return_status=True


            if(return_status==True):
                error_message = {}
                error_message['message'] = err
                return HttpResponse(json.dumps(error_message),content_type='application/json')


                
            userdataobj = UserData.objects.filter(username=username)
            referral_code = userdataobj[0].referral_code

            if(Events.objects.filter(event_code=received_parameters['event_code']).exists()):
                eventobj = Events.objects.filter(event_code=received_parameters['event_code'])
                event_referral_code = eventobj[0].referral_code
            
            else:
                error_message = {}
                error_message['message'] = "Event Code Not Found"
                return HttpResponse(json.dumps(error_message),content_type='application/json')


            if(referral_code == event_referral_code):

                if received_parameters['content']==None:
                    eventobj = Events.objects.filter(event_code = received_parameters['event_code'])
                    received_parameters['content'] = eventobj[0].certificate_default_content

                uid_number = secrets.token_hex(10)


                while Certificates.objects.filter(uid_number=uid_number).exists():
                    uid_number = secrets.token_hex(10)


                if Events.objects.filter(event_code=received_parameters['event_code']).exists():


                    if Certificates.objects.filter(event_code=received_parameters['event_code'], participant_id=received_parameters['participant_id']).exists():
                        error_message = {}
                        error_message['message'] = 'A certificate for that participant already exists'
                        return HttpResponse(json.dumps(error_message),content_type='application/json')
                    
                    else:
                        
                        eventobj = Events.objects.filter(event_code=received_parameters['event_code'])
                        template_number = str(eventobj[0].template_number)

                        print(template_number)
                        print(received_parameters['position'])

                        certificate_url,date_issued = testing_images.generate_certificate(uid_number,received_parameters['participant_name'],"off/",received_parameters['content'],received_parameters['position'],template_number)

                        certificate = Certificates.objects.create(uid_number=uid_number,event_code=received_parameters['event_code'],participant_name=received_parameters['participant_name'],participant_id=received_parameters['participant_id'],certificate_link=certificate_url,date_issued=date_issued,content=received_parameters['content'],position=received_parameters['position'])
                        certificate.save()

                        event_cert = Event_Certificates.objects.create(event_code=received_parameters['event_code'],uid_number=uid_number)

                        event_cert.save()

                        success_message = {}
                        success_message['message'] = 'User Succesfully Verified and Certificate Has been added'
                        success_message['certificate_url'] = certificate_url
                        return HttpResponse(json.dumps(success_message),content_type='application/json')

                else:
                    error_message = {}
                    error_message['message'] = 'This event doesnot exists'
                    return HttpResponse(json.dumps(error_message),content_type='application/json')
            else:
                error_message = {}
                error_message['message'] = 'UnAuthorized Action, The event code does not belong to this account'
                return HttpResponse(json.dumps(error_message),content_type='application/json')
            
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    # response_status = {}
    # response_status['message'] = 'Right now you are inside'

    # return HttpResponse(json.dumps(received_parameters),content_type="application/json")


def emailcertificate_view(request):

    print("inside emailcertificate view")

    received_parameters = {}
    received_parameters['name'] = request.GET.get('name',None)
    received_parameters['university'] = request.GET.get('university',None)
    received_parameters['event_code'] = request.GET.get('event_code',None)
    received_parameters['participant_id'] = request.GET.get('participant_id',None)
    received_parameters['email'] = request.GET.get('email',None)


    # return HttpResponse(json.dumps(received_parameters),content_type='application/json') #Data Received

    #To-do
    #Add authentication headers
    #Add database
    #Verify against database
    #Return the Url feteched, Firebase Storage or Postgres

    return HttpResponse(json.dumps(received_parameters),content_type="application/json")

    return HttpResponse("Data Received, no errors, database not added, will let you know if certificate if found, will send data")



def getevents_view(request):

    print("Inside get Events View")
    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    # login(username,password)
    # If username and password matched -> return sucess
    # Else return invalid credentials -> account not exists/they dont match

    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            userdataobj = UserData.objects.filter(username=username)
            referral_code = userdataobj[0].referral_code

            all_events = Events.objects.filter(referral_code=referral_code)
            all_events_json = serializers.serialize('json', all_events)

            success_message = {}
            success_message['message'] = 'User Succesfully Verified'
            print(type(all_events))
            print(all_events)
            return HttpResponse(all_events_json,content_type='application/json')
        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

def geteventcertificates_view(request):

    print("Inside get Event certificates View")
    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    # login(username,password)
    # If username and password matched -> return sucess
    # Else return invalid credentials -> account not exists/they dont match

    if User.objects.filter(username=username).exists():
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            received_parameters = {}
            received_parameters['event_code'] = request.GET.get('event_code',None)


            if(received_parameters['event_code']==None):
                error_message = {}
                error_message['message'] = "event code null"
                return HttpResponse(json.dumps(error_message),content_type='application/json')


            userdataobj = UserData.objects.filter(username=username)
            referral_code = userdataobj[0].referral_code

            if(Events.objects.filter(event_code=received_parameters['event_code']).exists()):
                eventobj = Events.objects.filter(event_code=received_parameters['event_code'])
                event_referral_code = eventobj[0].referral_code

                if(referral_code == event_referral_code):
                    all_event_certificates = Event_Certificates.objects.filter(event_code=received_parameters['event_code'])
                    
                    all_event_certificates_json = serializers.serialize('json', all_event_certificates)
                    return HttpResponse(all_event_certificates_json,content_type='application/json')
                else:
                    error_message = {}
                    error_message['message'] = 'UnAuthorized Action, The event code does not belong to this account'
                    return HttpResponse(json.dumps(error_message),content_type='application/json')
            else:
                error_message = {}
                error_message['message'] = 'The event code provided does not exists'
                return HttpResponse(json.dumps(error_message),content_type='application/json')

        else:
            error_message = {}
            error_message['message'] = 'Invalid Credentials'
            return HttpResponse(json.dumps(error_message),content_type='application/json')


    else:
        error_message = {}
        error_message['message'] = 'User Data Not Found!!!!'
        return HttpResponse(json.dumps(error_message),content_type='application/json')