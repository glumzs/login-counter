from django.db import models
import os

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

class UsersModel(models.Model):
	user = models.CharField(max_length=128)
	password = models.CharField(max_length=128)
	count = models.IntegerField()
	def login(self, user, password):
		print "GOT LOGIN: " + user + "/" + password
		try:
			res = UsersModel.objects.get(user=user,password=password)
			print "SUCCESS!@@@@ " + str(res.count)
		except UsersModel.DoesNotExist:
			res = None
		if res:
			res.count += 1
			res.save()
			return res.count
	
		return -1
	def add(self,user,password):
		if not (len(user) > 0 and len(user) <= 128):
			return ERR_BAD_USERNAME
		if len(password) > 128:
			return ERR_BAD_PASSWORD
		
		exists = UsersModel.objects.filter(user=user)
		if exists and exists[0]:
			return ERR_USER_EXISTS
		
		newuser = UsersModel(user=user,password=password,count=1)
		newuser.save()
		return 1
		
	def TESTAPI_resetFixture(self):		
		u = UsersModel.objects.all()
		u.delete()
		return 1
	
