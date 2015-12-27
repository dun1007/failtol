#!/usr/bin/env python
'''
  Assignment 3 Delete operation.

  Author : Steve Yoo
'''

# Library packages
import os
import re
import sys
import json
import os.path

# Installed packages
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import HashKey

from bottle import route, run, request, response, abort, default_app, HTTPResponse

AWS_REGION = "us-west-2"
QUERY_PATTERN = "^(id=[0-9]+|name=[a-zA-Z]+)$"
PORT = 8080
query_regex = re.compile(QUERY_PATTERN)


def delete(request):
	# check if query string matches regex, specifying only id or name
	if not query_regex.match(request.query_string):
		abort(400, "Query string does not match pattern '{0}'".format(QUERY_PATTERN))
	
	# commence to delete operation
	return do_delete(request)

def do_delete(request):
	print("trying to delete")
	id = int(request.query.id)
	name = request.query.name
	a3Table = Table('assignment_3', connection = boto.dynamodb2.connect_to_region(AWS_REGION))


	return_message_success = { "data" : { "type" : "person", "id" : str(id) } }
	return_message_failure = { "errors" : [ { "not_found" : { "id" : str(id) } } ] }

	try:
		item = a3Table.get_item(id=id)
		if item.delete():
			print("delete successful")
			return HTTPResponse(status = 200, body=return_message_success)
		else:
			print("delete failed")
			raise Exception("Item Does Not Exist")
	except Exception as err:
		print('error, {0}'.format(err))
		return HTTPResponse(status = 404, body=return_message_failure)


