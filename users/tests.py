"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from users.models import UsersModel

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

class UsersUnitTest(TestCase):
	def test_add_new(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
	def test_add_duplicate(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.add("test123","pass123")
		self.assertEqual(ret,ERR_USER_EXISTS)
	def test_add_two(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.add("test1234","pass123")
		self.assertEqual(ret,SUCCESS)
	def test_add_empty(self):
		u = UsersModel()
		ret = u.add("","pass123")
		self.assertEqual(ret,ERR_BAD_USERNAME)
	def test_long_username(self):
		u = UsersModel()
		uname = "a"*129
		ret = u.add(uname,"pass123")
		self.assertEqual(ret,ERR_BAD_USERNAME)
	def test_long_password(self):
		u = UsersModel()
		password = "a"*129
		ret = u.add("test123",password)
		self.assertEqual(ret,ERR_BAD_PASSWORD)
	def test_login(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.login("test123","pass123")
		self.assertEqual(ret,2)
	def test_wrongpassword(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.login("test123","pass1234")
		self.assertEqual(ret,ERR_BAD_CREDENTIALS)
	def test_wronguser(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.login("test1234","pass1234")
		self.assertEqual(ret,ERR_BAD_CREDENTIALS)
	def test_login2(self):
		u = UsersModel()
		ret = u.add("test123","pass123")
		self.assertEqual(ret,SUCCESS)
		ret = u.login("test123","pass123")
		self.assertEqual(ret,2)
		ret = u.login("test123","pass123")
		self.assertEqual(ret,3)
