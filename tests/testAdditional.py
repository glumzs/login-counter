import unittest
import os
import testLib

class TestLogin(testLib.RestTestCase):
    """Test login"""
    def assertResponse(self, respData, count = None, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 2)
    def testWrongLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : 'password'} )
        self.assertResponse(respData, errCode = -1)
        
	def testWrongPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
		self.assertResponse(respData, count = 1)

		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password222'} )
		self.assertResponse(respData, errCode = -1)

