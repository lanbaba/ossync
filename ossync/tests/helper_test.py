# -*- coding: utf-8 -*-

import os, sys
import unittest
from ..lib import helper

class TestHelper(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def tearDown(self):
		pass
		
	def testWalkFiles(self):
		root = '/Volumes/Macintosh HD 2/software'
		files = list(helper.walk_files(root, yield_folders = True))
		self.assertEqual(len(files) > 0, True)
		
	def testCalcFileMd5(self):
		filepath = '/Users/wuts/work/ossync/ossync/tests/api_test.py'
		hashstr =  helper.calc_file_md5(filepath)
		print hashstr
		self.assertEqual(hashstr.upper(), 'ACC853492102F896787C2B9AAB3C766C')

	
