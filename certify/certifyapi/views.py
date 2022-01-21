from django.http import HttpResponse
from django.shortcuts import render
import json



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

    #Do the logic to add user to an organisation based on referral code, if referral code not found do necessary things etx


    response_status = {}
    response_status['message'] = 'Right now you are inside'

    return HttpResponse(json.dumps(response_status),content_type="application/json")

