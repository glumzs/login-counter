from django.db import models

class UsersModel(models.Model):
	user = models.CharField(max_length=128)
	password = models.CharField(max_length=128)
	count = models.IntegerField()
	def login(self, user, password):
		try:
			res = UsersModel.objects.get(user=user,password=password)
		except UsersModel.DoesNotExist:
			res = None
		if res:
			res.count += 1
			res.save()
			return res.count
	
		return -1
	def add(self,user,password):
		if not (len(user) > 0 and len(user) <= 128):
			return -3
		if len(password) > 128:
			return -4
		
		exists = UsersModel.objects.filter(user=user)
		if exists and exists[0]:
			return -2
		
		newuser = UsersModel(user=user,password=password,count=1)
		newuser.save()
		return 1
		
	def TESTAPI_resetFixture(self):		
		u = UsersModel.objects.all()
		u.delete()
		return 1

