from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from users.models import UsersModel

#from users.models import UsersModel

def index(request):
    return HttpResponse("Hello, world.")
    
def login(request):
	if request.method == "POST":
		req = simplejson.loads(request.raw_post_data)
		u = UsersModel()
		ret = u.add(req['user'],req['password'])
	response_data['errCode'] = 0
	response_data['count'] = 1
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
		#return HttpResponse("ok")
	else:
		return HttpResponse(simplejson.dumps(result), mimetype='application/json')
