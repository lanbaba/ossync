# -*- coding: utf-8 -*-

import sys
from ..lib import queue_model
import hashlib
import unittest

class TestQueueModel(unittest.TestCase):
	
	def setUp(self):
		dbpath =  'db/ossync.db'
		self.queue_model = queue_model.QueueModel(dbpath)
		self.queue_model.open()

	def tearDown(self):
		self.queue_model.close()
	
	def testSave(self):
		data = {
            "root": '/Users/wuts/newwork/ossync',
            "relpath": 'docs/OSS_API.pdf',
            "bucket": 'dzdata',
            "action": 'C',
            "status": 1,
            "retries": 0,
        }
		m = hashlib.md5()
		m.update(data['root'] + data['relpath'] + data['bucket'])
		hashcode = m.hexdigest()
		self.queue_model.save(data)
		res = self.queue_model.get(hashcode)
		self.assertNotEqual(res, None)

	def testGet(self):
		res = self.queue_model.get('e94bdba1f90e768442f2fa6d036428db')
		# print res['root']
		self.assertNotEqual(res, None)
		
	def testFindAll(self):
		res = self.queue_model.find_all(status = 1)
		# print res
		self.assertNotEqual(res, None)
	
	def testUpdateStatus(self):
		self.queue_model.update_status('e94bdba1f90e768442f2fa6d036428db', 1)
		res = self.queue_model.get('e94bdba1f90e768442f2fa6d036428db')
		self.assertEqual(res['status'], 1)
		
	def testUpdateAction(self):
		self.queue_model.update_action('e94bdba1f90e768442f2fa6d036428db', 'M')
		res = self.queue_model.get('e94bdba1f90e768442f2fa6d036428db')
		self.assertEqual(res['action'], 'M')
		
	def testUpdateRetries(self):
		self.queue_model.update_retries('e94bdba1f90e768442f2fa6d036428db', 2)
		res = self.queue_model.get('e94bdba1f90e768442f2fa6d036428db')
		self.assertEqual(res['retries'], 2)
		
	"""
	def testDelete(self):
		self.queue_model.delete('b875fa0086d8af47a3a0126c91d6133f') 
		res = self.queue_model.get('b875fa0086d8af47a3a0126c91d6133f')
		self.assertEqual(res, None)
	"""	
		

