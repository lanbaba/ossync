# -*- coding: utf-8 -*-

import sys, time, md5
from xml.dom import minidom
from ..sdk import oss_api
from ..sdk import oss_xml_handler
import hashlib
import unittest

class TestOssApi(unittest.TestCase):
	
	def setUp(self):
		HOST = "storage.aliyun.com"
		ACCESS_ID = "ACSAu8DDXiZ4e23d"
		SECRET_ACCESS_KEY = "xyZ9mBgXtG"
		self.GetBufferSize = 1024*1024*10
		self.oss = oss_api.OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
		if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
			print "Please set ACCESS_ID and SECRET_ACCESS_KEY"
			exit(0)
		
	def tearDown(self):
		pass
		
	def testGetService(self):
		res = self.oss.get_service() 
		if(res.status / 100 == 2):
			body = res.read()
			h = oss_xml_handler.GetServiceXml(body)
			print "buckect list size is: ", len(h.list())
			print "buckect list is:"
			for i in h.list():
				print i[0]
		else:
			print res.status 
		self.assertEqual(res.status / 100, 2)
		
	def getObjectToFile(self):
		filename = 'favicon.ico'
		res = self.oss.get_object_to_file(bucket = 'dzdata', object = 'forum/favicon.ico', filename = filename, headers = {})
		'''if(res.status / 100 == 2):
			print 'get object success'
			data = res.read(self.GetBufferSize)
			print data
		else:
			print 'get object failure'
		'''
		self.assertEqual(res.status / 100, 2)
		
	def testGetObject(self):
		res = self.oss.get_object(bucket = 'dzdata', object = 'docs/mmmmm/favicon.ico', headers = {})
		'''if(res.status / 100 == 2):
			print res.getheader('Etag')
			print res.read()
		else:
			print 'head object failure'
		'''
		self.assertEqual(res.status / 100, 2)
		
	def testHeadObject(self):
		res = self.oss.head_object(bucket = 'dzdata', object = 'docs/mmmmm/favicon.ico', headers = {})
		'''if(res.status / 100 == 2):
			print res.getheader('Etag')
			print res.msg
			print res.reason
		else:
			print 'head object failure'
		'''
		self.assertEqual(res.status / 100, 2)
		
	'''
	def testPutObjectFromString(self):
		somestr = ""
		# print self._calcStrMd5(somestr).upper()
		res = self.oss.put_object_from_string(bucket = 'dzdata', object = 'forum/xmun/', input_content = somestr, content_type = "text/plain",  headers = {})
		# print res.getheader('Etag')
		self.assertEqual(res.status / 100, 2)
	'''
		
	def testDeleteObject(self):
		res = self.oss.delete_object('dzdata', 'docs/mmmmm/', {})
		'''if(res.status == 200):
			print 'delete object success'
		else:
			print 'delete object failure'
			print res.status
		'''
		print res.status
		self.assertEqual(res.status / 100, 2)
		
	def testPutObjectFromFile(self):
		filepath = '/Users/wuts/work/ossync/ossync/tests/api_test.py'
		hashstr = self._calcFileMd5(filepath).upper()
		# print hashstr
		res = self.oss.put_object_from_file(bucket = 'dzdata', object = 'ossync/tests/api_test.py', filename = filepath, content_type = "text/plain",  headers = {})
		# print res.getheader('Etag')
		'''if(res.status == 200):
			print res.getheader('Etag') 
			print 'put object from string success' 
		else:
			print 'put object from string failure'
			print res.status
		'''
		self.assertEqual(res.status / 100, 2)
		
		
	def testGetBucket(self):
		result = []
		bucket = 'privdata'
		delimiter = '/'
		prefix = 'images/'
		marker = ''
		headers = {}
		maxkeys = ''
		self._walk_bucket( bucket, prefix, marker, delimiter, maxkeys, headers, result)
		print result
		self.assertEqual(len(result) > 0, True)
	
	def testCreateBucket(self):
		bucket = 'myosdata'
		headers = {}
		acl = ''
		res = self.oss.create_bucket(bucket, acl, headers) 
		self.assertEqual(res.status / 100, 2)
		
	def _walk_bucket(self, bucket, prefix, marker, delimiter, maxkeys, headers, result = []):
		res = self.oss.get_bucket(bucket, prefix, marker, delimiter, maxkeys, headers)
		if (res.status / 100) == 2:
			body = res.read()
			h = oss_xml_handler.GetBucketXml(body)
			(file_list, common_list) = h.list() 
			if len(file_list) > 0:
				for item in file_list:
					result.append(item[0])
			if len(common_list) > 0: 
				for path in common_list: 
					result.append(path)
					self._walk_bucket(bucket, path, marker, delimiter, maxkeys, headers, result) 
		
	
	def _calcStrMd5(self, somestr):
		md5obj = hashlib.md5()
		md5obj.update(somestr)
		hashstr = md5obj.hexdigest()
		return hashstr
		
	def _calcFileMd5(self, filepath):
		with open(filepath, 'rb') as f:
			md5obj = hashlib.md5()
			md5obj.update(f.read())
			hashstr = md5obj.hexdigest()
			return hashstr	

