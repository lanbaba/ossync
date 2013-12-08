# -*- coding: utf-8 -*-

# Copyright (c) 2012 Wu Tangsheng(lanbaba) <wuts73@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, threading, logging
import os.path
from Queue import *
import hashlib
from ossync.lib import helper
from ossync.lib import queue_model

class QueueThread(threading.Thread):
	
	""" 此线程的作用是将bucket,root, path压入要上传的队列，队列元素格式：
	   "bucket::root::relpath::action::life"
	   其中action表示文件是新建还是修改还是删除;life表示重入次数
	"""
	def __init__(self, bucket, dirs, queue, *args, **kwargs):
		threading.Thread.__init__(self, *args, **kwargs)
		self.bucket = bucket
		self.queue = queue
		self.dirs = dirs
		
		self._terminate = False
		self.logger =  logging.getLogger('app')
		dbpath =  'db/ossync.db'
		self.qm = queue_model.QueueModel(dbpath)
		
	def terminate(self):
		self._terminate = True
		
	def is_el_queued(self, hashcode):
		row = self.qm.get(hashcode)
		if row:
			return True
		return False
	
	def run(self):
		files = {}
		for d in self.dirs:
			files[d] = list(helper.walk_files(os.path.normpath(d), yield_folders = True))
		if len(files) > 0:
			self.qm.open()
			self.logger.info('Queue path ...') 
			for i in files:
				if len(files[i]) > 0:
					for path in files[i]:
						relpath = os.path.relpath(path, i) # 相对于root的相对路径 
						el = self.bucket + '::' + i+ '::' + relpath + '::C'
						hashcode = helper.calc_el_md5(i, relpath, self.bucket)
						if not self.is_el_queued(hashcode): 
							data={"root": i, "relpath": relpath, "bucket": self.bucket, "action": 'C', "status":  0, "retries" : 0}
							self.qm.save(data)
							'''queue el, el: element of queue , formated as "bucket::root::path"'''
							try:
								self.queue.put(el, block = True, timeout = 1)
								msg = 'queue element:' + el
								#print msg
								self.logger.info(msg)
							except Full as e:
								self.queue.put(None)
								self.logger.error(e.message) 
			self.qm.close()
		self.queue.put(None)
		#self.queue.join()
		return
		
			
					
			
		