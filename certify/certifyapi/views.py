from django.http import HttpResponse
from django.shortcuts import render
import json
import secrets


from django.contrib import auth


#Importing Databases
from certifyapi.models import Referrals, UserData
from django.contrib.auth.models import User


from django.core.mail import send_mail


# Create your views here.

def verifycertificate_view(request):

    print("inside verifycertificate view")

    received_parameters = {}

    received_parameters['uid_number'] = request.GET.get('uid_number',None)

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


    verification_status = {}
    verification_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(verification_status),content_type="application/json")
    
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


    referral = Referrals.objects.create(name=received_parameters['name'],university=received_parameters['university'],email=received_parameters['email'],reason=received_parameters['email'],referral_code=new_referral_code)
    referral.save()

    success_message = {}
    success_message['message'] = 'Your referral code is generated and is under pending state, we will get back to you once it is generated. This is a normal check to keep server from spamming. You will receive a mail if we found its legit.'
    
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

    

    response_status = {}
    response_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(response_status),content_type="application/json")

def registerevent_view(request):

    print("Inside addevent view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    received_parameters = {}
    received_parameters['event_name'] = request.GET.get('event_name',None)
    received_parameters['event_code'] = request.GET.get('event_code',None)
    received_parameters['content'] = request.GET.get('content',None)
    

    response_status = {}
    response_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(received_parameters),content_type="application/json")

def addcertificate_view(request):

    print("Inside addcertificate view")

    
    try:
        username = request.META['HTTP_USERNAME']
        password = request.META['HTTP_PASSWORD']

    except:
        error_message = {}
        error_message['message'] = 'Could not find username/password in headers'
        return HttpResponse(json.dumps(error_message),content_type='application/json')

    received_parameters = {}
    received_parameters['event_code'] = request.GET.get('event_code',None)
    received_parameters['participant_name'] = request.GET.get('participant_name',None)
    received_parameters['participant_id'] = request.GET.get('participant_id',None)
    

    response_status = {}
    response_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(received_parameters),content_type="application/json")


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
