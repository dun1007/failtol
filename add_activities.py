#!/usr/bin/env python

import boto.dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from bottle import HTTPResponse

def add_activities(request):
	uid = request.query.id
	activities = request.query.activities.split(',')
	
	table = Table('assignment_3',connection=boto.dynamodb2.connect_to_region('us-west-2'))
	
	try:
		#get the item from the DB with the corresponding ID
		item = table.get_item(id=uid)
		
		#update activities to include new activities.
		if(item['activities']):
			item['activities'] = activities + list(set(item['activities']) - set(activities))
		else:
			item['activities'] = activities
		item.partial_save()
		
		successJson = {
			"data": {
				"type": "person",
    			"id": str(id),
    			"name": item['name'],
    			"activities": item['activities']
			}
		}
		
		return HTTPResponse(status = 200, body = successJson)
		
	except boto.dynamodb2.exceptions.ItemNotFound:
		failureJson = {
		  "errors": [{
			 "not_found": {
				"id": str(uid)
			  }
		  }]
		}
		
		return HTTPResponse(status = 404, body = failureJson);