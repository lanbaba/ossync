# coding: utf-8

import hashlib

def calcMd5(filepath):
	with open(filepath, 'rb') as f:
		md5obj = hashlib.md5()
		md5obj.update(f.read())
		hashstr = md5obj.hexdigest()
		return hashstr
		
if __name__ == '__main__':
	filepath = '/Users/wuts/work/ossync/ossync/tests/api_test.py'
	print calcMd5(filepath)
		