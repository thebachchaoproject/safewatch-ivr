from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import json
import time, os
from django.core import serializers
from datetime import datetime
import os.path
import urllib, urllib2
import plivoxml
from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import patterns, url

import plivo

# To Handle Rest API..!!!
#from django_rest_framework import rest_framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# To connect with DB..!!!
from django.db import connection, transaction

# To get all Models of the application..!!!
from safewatch_ivr_app.models import Submit_report

# This is for python 3 [ to work with local modules ]..!!!
import sys
sys.path.append('/safewatch_ivr_app/')

# Local Utilities..!!!
from safewatch_ivr_app.Utilities import utils
from safewatch_ivr_app.Utilities import WritingToJson

# Local Modules..!!!
#from safewatch_ivr_app.Modules import 

# This file will be played when a caller presses 2.
PLIVO_SONG = "https://s3.amazonaws.com/plivocloud/music.mp3"

# This is the message that Plivo reads when the caller dialN4Vs342js in
IVR_MESSAGE = "Welcome to the Plivo IVR Demo App. Press 1 to hear a random \
                joke. Press 2 to listen to a song."

# This is the message that Plivo reads when the caller does nothing at all
NO_INPUT_MESSAGE = "Sorry, I didn't catch that. Please hangup and try again \
                    later."

# This is the message that Plivo reads when the caller inputs a wrong number.
WRONG_INPUT_MESSAGE = "Sorry, it's wrong input."

URLS_FOR_APIS = "YOUR_SERVER_URL"

URLS_FOR_AUDIOS = "YOUR_SERVER_URL_and_PATH_TO_FILES"

@csrf_exempt 
@api_view(['GET', 'POST'])
#To play the 1st question.
def FirstQ(request):
	response = plivoxml.Response()
	if request.method == 'GET':
		#getdigits_action_url = url('ivr', _external=True)
		getDigits = plivoxml.GetDigits(action=URLS_FOR_APIS+'firstq/',
										method='POST', timeout=10, numDigits=1,
										retries=2)
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		response.add(getDigits) 
		response.addSpeak(NO_INPUT_MESSAGE)

		return HttpResponse(str(response), content_type = "application/xml")

	elif request.method == 'POST':
		digit = request.POST['Digits']
		print request.POST
		
		getDigits = plivoxml.GetDigits(action=URLS_FOR_APIS+'secondq/',
										method='POST', timeout=10, numDigits=2,
										retries=2)
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		response.add(getDigits)
		response.addSpeak(NO_INPUT_MESSAGE)
		data = {}
		if digit == "1":
			data = {'gender' : 'male'}
		elif digit == "2":
			data = {'gender' : 'female'}
		elif digit == "3":
			data = {'gender' : 'other'}
		else:
			response.addSpeak(WRONG_INPUT_MESSAGE)
		if data != {}:
			cursor = connection.cursor()
			cursor.execute("INSERT INTO safewatch_ivr_app_submit_report (call_id, called_to, gender) VALUES(%s, %s, %s)", [request.POST['CallUUID'], request.POST['To'], data['gender']])

		return HttpResponse(str(response), content_type = "application/xml")
		

@csrf_exempt 
@api_view(['GET', 'POST'])
def SecondQ(request):
	response = plivoxml.Response()
	if request.method == 'POST':
		digit = request.POST['Digits']
		getDigits = plivoxml.GetDigits(action=URLS_FOR_APIS+'thirdq/',
										method='POST', timeout=10, numDigits=1,
										retries=2)
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")

		response.add(getDigits)
		response.addSpeak(NO_INPUT_MESSAGE)
		data_temp = {}
		if (len(digit) > 1 and len(digit) <= 3):
			data_temp = {'Age' : digit}
			call_id = request.POST['CallUUID']
			called_to = request.POST['To']
		else:
			response.addSpeak(WRONG_INPUT_MESSAGE)
			
		if data_temp != {}:
			try:
				cursor = connection.cursor()
				cursor.execute("UPDATE safewatch_ivr_app_submit_report SET age = %s WHERE call_id = %s AND called_to = %s", [digit, call_id, called_to])
			except Exception, e:
				print e	

	return HttpResponse(str(response), content_type = "application/xml")
		

@csrf_exempt 
@api_view(['GET', 'POST'])
def ThirdQ(request):
	response = plivoxml.Response()
	if request.method == 'POST':
		digit = request.POST['Digits']
		getDigits = plivoxml.GetDigits(action=URLS_FOR_APIS+'thirdq/',
										method='POST', timeout=10, numDigits=1,
										retries=2)
		getDigits.addPlay(URLS_FOR_AUDIOS+"you_rec_filename")
		data_temp = {}
		if digit:
			data_temp = {'incident_category' : digit}
			call_id = request.POST['CallUUID']
			called_to = request.POST['To']
		else:
			response.addSpeak(WRONG_INPUT_MESSAGE)
			
		if data_temp != {}:
			try:
				cursor = connection.cursor()
				cursor.execute("UPDATE safewatch_ivr_app_submit_report SET incident_category = %s WHERE call_id = %s AND called_to = %s", [digit, call_id, called_to])
			except Exception, e:
				print e	
		
		return HttpResponse(str(response), content_type = "application/xml")		
		

@csrf_exempt
# TO store the missed call and make a call to that number..!!!
def MakeCall(request):
	
	response_data = {}
	if request.method == 'POST':
		auth_id = "YOUR_AUTH_ID"
		auth_token = "YOUR_AUTH_TOKEN"
		
		try:
			if request.POST['to'] == ( "" or None or 0):
				response_data['result'] = 'Failed'
				response_data['reason'] = 'Not a valid Number to call'
				return HttpResponse(json.dumps(response_data), content_type = "application/json")
			to_no = request.POST['to']
		except:
			response_data['result'] = 'Failed'
			response_data['reason'] = 'Not a valid post request'
			return HttpResponse(json.dumps(response_data), content_type = "application/json")	

		p = plivo.RestAPI(auth_id, auth_token)

		params = {
			'to': request.POST['to'], # The phone numer to which the all has to be placed
			'from' : request.POST['from'], # The phone number to be used as the caller id
			'answer_url' : URLS_FOR_APIS+'firstq/', # The URL invoked by Plivo when the outbound call is answered
			'answer_method' : "GET", # The method used to call the answer_url
			# Example for Asynchrnous request
			'hangup_url' : URLS_FOR_APIS+'storedata/',
			'hangup_method' : "POST",
			#'callback_url' : "" # The URL notified by the API response is available and to which the response is sent.
			#'callback_method' : "GET" # The method used to notify the callback_url.
		}

		# Make an outbound call
		response = p.make_call(params)
		return HttpResponse(str(response))
	else:
		response_data['result'] = 'Failed'
        response_data['reason'] = 'Not a valid post request'
        return HttpResponse(json.dumps(response_data), content_type = "application/json")

@csrf_exempt0
def StoreData(request):
	print request.POST
	return
