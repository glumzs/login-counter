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
			response_data = {"errCode" : SUCCESS, "count" : ret}
	
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	
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
	result = {"output":"1", "totalTests": 10, "nrFailed": 0}
	if request.method == "POST":
		(ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
		try:
			errMsg = ""  
			output = ""     # Some default values
			totalTests = 0
			nrFailed   = 0
			while True:  # Give us a way to break
				# Find the path to the server installation
				thisDir = os.path.dirname(os.path.abspath(__file__))
				print ofileName
				cmd = "python manage.py test users >" + ofileName + " 2>&1 "
				print "Executing "+cmd
				#code = os.system(cmd)
				#time.sleep(3)
				#code = subprocess.call(cmd,shell=True)
				(output, err) = Popen(cmd,  stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True).communicate(None)
				code = 0
				if code != 0:
					# There was some error running the tests.
					# This happens even if we just have some failing tests
					errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
					# Continue to get the output, and to parse it

				# Now get the output
				try:
					ofileFile = open(ofileName, "r")
					output = ofileFile.read()
					ofileFile.close()
				except:
					errMsg += "Error reading the output "+traceback.format_exc()
					# No point in continuing
					break

				print "Got "+output + " ouch"
				# Python unittest prints a line like the following line at the end
				# Ran 4 tests in 0.001s
				m = re.search(r'Ran (\d+) tests', output)
				if not m:
					errMsg += "Cannot extract the number of tests\n"
					break
				totalTests = int(m.group(1))
				# If there are failures, we will see a line like the following
				# FAILED (failures=1)
				m = re.search('rFAILED.*\(failures=(\d+)\)', output)
				if m:
					nrFailures = int(m.group(1))
					break # Exit while

			# End while
			result = { 'output' : errMsg + output,
						'totalTests' : totalTests,
						'nrFailed' : nrFailed }

			return HttpResponse(simplejson.dumps(result), mimetype='application/json')               
		finally:
			print "hmm"
			#os.unlink(ofileName)
		#cmd = "python manage.py test users >" + ofileName + "2>&1 &"
		#os.system(cmd)
		#script(cmd)
		#r = subprocess.call(cmd,Shell=True)
		return HttpResponse(simplejson.dumps(result), mimetype='application/json')
	else:
		return HttpResponse("Hello, world.")
