# -*- coding: utf-8 -*-

import os, sys
def cur_dir():
	path = sys.path[0]
	print path
	if os.path.isdir(path):
		return path
	elif os.path.isfile(path):
		return os.path.dirname(path)
		
if __name__ == '__main__':
	print cur_dir()
		