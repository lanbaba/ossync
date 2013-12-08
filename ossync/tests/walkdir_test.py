# -*- coding: utf-8 -*-

import os, sys
from os.path import *
from Queue import *
sys.path.append("/Users/wuts/src/python/ossync/lib")
from walkdir import walk_files
files = list(walk_files(root = "/Volumes/Macintosh HD 2/software", yield_folders = True))
queue = Queue(100)
print queue.qsize()
for path in files:
	try:
	    queue.put(path, block = True, timeout = 1)
	except Full as e:
		print e
		break
print "get queue:"
while not queue.empty():
	item = queue.get(block = True, timeout = 1)
	print item