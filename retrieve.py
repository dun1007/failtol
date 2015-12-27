'''
  Handles the "retrieve" operation for CMPT 474 Assignment 3.

  Author: Matthew Chan
'''

# Library packages
import os
import re
import sys
import json

# Installed packages
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey

from bottle import route, run, request, response, abort, default_app, HTTPResponse

AWS_REGION = "us-west-2"
QUERY_PATTERN = "^(id=[0-9]+|name=[a-zA-Z]+)$"
PORT = 8080

query_regex = re.compile(QUERY_PATTERN)

def retrieve(request):
	# check if query string matches regex, specifying only id or name
	if not query_regex.match(request.query_string):
		abort(400, "Query string does not match pattern '{0}'".format(QUERY_PATTERN))

	# otherwise if matches, go ahead and perform the actual retrieval 
	return do_retrieve(request)

def do_retrieve(request):
	id = int(request.query.id)
	name = request.query.name

	table = Table('assignment_3', connection = boto.dynamodb2.connect_to_region(AWS_REGION))

	data = table.get_item(id=id)
	print('values: {0}, {1}, {2}'.format(data['id'], data['name'], data['activities']))

	try:
		# if request is based on user id
		if id is not None:
			# retrieve item from database with this id
			item = table.get_item(id=id)

		# if request is based on name
			# code to follow later

		# parse activities string into list of strings
		# activities = item['activities'].split(',')

		# create response json object
		successJson = {
			"data": {
				"type": "person",
    			"id": str(id),
    			"name": item['name'],
    			"activities": item['activities']
			}
		}

		print('success json: ' + json.dumps(successJson))

		# if no error found, return status code 200 with the success json
		return HTTPResponse(status = 200, body = successJson)

	except Exception as e:
		# print error code here
		print('error, {0}'.format(e))
		
		# create response json object
		errorJson = {
			"errors": [{
		     	"not_found": {
		        	"id": str(id)
		      	}
		  	}]
		}

		# if error found, return status code 404 with error json
		return HTTPResponse(status = 404, body = errorJson);






