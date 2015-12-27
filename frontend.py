#!/usr/bin/env python

'''
  Front end Web server for CMPT 474 Assignment 3.
  Derived from code by Ted Kirkpatrick.

  Edwin Gao (yga22)
  Jacky Chao (chaojiac)
  Hyun Suk Yoo (hsyoo)
  Matthew Chan (machan)
'''

# Library packages
import os
import re
import sys
import json

from bottle import route, run, request, response, abort, default_app


AWS_REGION = "us-west-2"
QUERY_PATTERN = "/*"

PORT = 8080

query_pattern = re.compile(QUERY_PATTERN)

# Everyting below returns hardcoded data. #
@route('/create')
def create():
    # Call create(request) from create.py #
    from create import create
    return create(request)

@route('/delete')
def delete():
    from delete import delete
    return delete(request)

@route('/add_activities')
def add_activities():
    data = {
        "id" : "123456789",
        "name" : "Catelyn_Tully",
        "activities" : [
            "defending",
            "advising",
            "care_giving",
            "lurking",
        ]
    }
        
    
    
    from add_activities import add_activities
    return add_activities(request)

@route('/retrieve')
def retrieve():
    data = {
        "id" : "123456789",
        "name" : "Catelyn_Tully",
        "activities" : [
            "defending",
            "advising",
            "care_giving",
            "lurking",
        ]
    }
    
    # call retrieve function to fetch the item based on the query string
    from retrieve import retrieve
    return retrieve(request)

# Error handling not working yet. #
#@route('/*')
#def any():
#    abort(400, "Query string does not match pattern")

# Runs the server in loop. #
app = default_app()
run(app, host="localhost", port=PORT)
