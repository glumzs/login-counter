import os
import re
import tempfile
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from users.models import UsersModel
from subprocess import *
import subprocess
import time

def script(script_text):
     p = Popen(args=script_text,
               shell=True)

     output, errors = p.communicate()
     return output, errors


def index(request):
    return HttpResponse("Hello, world.")
    
def login(request):
	if request.method == "POST":
		req = simplejson.loads(request.raw_post_data)
		u = UsersModel()
		ret = u.login(req['user'],req['password']) 
		if ret < 0:
			response_data = {"errCode": ret}
		else:
			response_data = {"errCode" : 1, "count" : ret}
	
		return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
	
def add(request):
	if request.method == "POST":
		req = simplejson.loads(request.raw_post_data)
		u = UsersModel()
		ret = u.add(req['user'],req['password'])
		errCode = 1
		count = 0
		if ret > 0:
			count = ret
		else:
			errCode = ret
		result = {"errCode": errCode, "count": count}
		return HttpResponse(simplejson.dumps(result), mimetype='application/json')
	
def resetFixture(request):
	result = []
	result.append({"errCode":"1"})

	if request.method== "POST":
		u = UsersModel()
		u.TESTAPI_resetFixture()
		return HttpResponse(simplejson.dumps(result), mimetype='application/json')
	else:
		return HttpResponse(simplejson.dumps(result), mimetype='application/json')
		
def unitTests(request):
	if request.method == "POST":
		errMsg = ""  
		output = ""     # Some default values
		totalTests = 0
		nrFailed   = 0
		cmd = "python manage.py test users"
		print "Executing "+cmd
		output = subprocess.check_output("python manage.py test users", shell=True,stderr=subprocess.STDOUT)

		print output
		m = re.search(r'Ran (\d+) tests', output)
		if not m:
			errMsg += "Cannot extract the number of tests\n"
		
		totalTests = int(m.group(1))
		# If there are failures, we will see a line like the following
		# FAILED (failures=1)
		m = re.search('rFAILED.*\(failures=(\d+)\)', output)
		if m:
			nrFailures = int(m.group(1))
		result = { 'output' : errMsg + output,
						'totalTests' : totalTests,
						'nrFailed' : nrFailed }

		return HttpResponse(simplejson.dumps(result), mimetype='application/json')    
