#!/usr/bin/env python

'''
  Create API call for CMPT 474 Assignment 3.

  Edwin Gao (yga22)
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
QUERY_PATTERN = "^id=[0-9]+&name=[a-zA-Z]+&activities=.*$"

PORT = 8080

query_pattern = re.compile(QUERY_PATTERN)

# Front-facing function #
def create(request):
	if not query_pattern.match(request.query_string):
		abort(400, "Query string does not match pattern '{0}'".format(QUERY_PATTERN))

	return do_create(request)

def do_create(request):
	# Break request into individual variables. #
	id = int(request.query.id)
	name = request.query.name
	activities = request.query.activities.split(',')

	# Call the table #
	a3Table = Table('assignment_3', connection = boto.dynamodb2.connect_to_region(AWS_REGION))
	
	# Construct python dict from parameters #
	data = {
		"id" : id,
		"name" : name,
		"activities" : activities
	}

	# Attempt a write into database #
	try:
		a3Table.put_item(data)
		return HTTPResponse(status = 201, body = success_json(id))

	# If id is already in database #
	except Exception as e:
		# Pull the entry so we can check #
		item = a3Table.get_item(id=id)

		# Check if existing entry is same as what we're trying to put in #
		if (item['id'] == id and item['name'] == name and item['activities'] == activities):
			return HTTPResponse(status = 201, body = success_json(id))
		
		# If the check fails, we know the details of the item are different #
		else:
			return HTTPResponse(status = 400, body = failure_json(id, name, activities))

# Helper function for success json #
def success_json(id):
	success = {
		"data" : {
			"type" : "person",
			"id" : id,
			"links" : {
				"self" : "http://localhost:8080/retrieve?id={0}".format(id)
			}
		}
	}
	return success

# Helper function for failure json #
def failure_json(id, name, activities):
	err = {
		"errors" : [{
			"id_exists" : {
				"status" : "400",
				"title" : "id already exists",
				"detail" : {
					"name" : name,
					"activities" : activities
				}
			}
		}]
	}
	return err