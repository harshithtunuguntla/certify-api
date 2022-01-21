from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.

def verifyuid(request,verify_uid):
    print("hello")
    # print(request.META['HTTP_URL'])

    verification_status = {}
    verification_status['status'] = '200'
    verification_status['response'] = 'OK'
    verification_status['message'] = 'verified'

    return HttpResponse(json.dumps(verification_status),content_type='application/json')