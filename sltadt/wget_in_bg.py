# -*- coding: utf-8 -*-


__author__ = 'GoTLiuM InSPiRIT <gotlium@gmail.com>'


import os
import sys
import grab
import urlparse


wget_cmd = "nohup wget -c --connect-timeout=5 --random-wait " \
	   "--no-check-certificate --retry-connrefused -t 0 " \
	   "'%(link)s' -O '%(filename)s' >& '%(filename)s.log' &"
link = sys.argv[1]
path = urlparse.urlparse(link).path
filename = os.path.join(os.getcwd(), os.path.basename(path))


def check_length():
	g = grab.Grab(nobody=True)
	g.go(link)
	length = int(g.response.headers['Content-Length'])
	local_length = os.path.getsize(filename)
	if length == local_length:
		return True
	return False


def download():
	os.system(wget_cmd % globals())


def rename():
	fs = str(globals()['filename']).split('.')
	counter_part = fs[-2].split('---')
	while True:
		if len(counter_part) > 1:
			counter_part[1] = str(int(counter_part[1]) + 1)
		else:
			counter_part.append('1')
		fs[-2] = '---'.join(counter_part)
		new_file = '.'.join(fs)
		if os.path.exists(new_file):
			counter_part = new_file.split('.')[-2].split('---')
			continue
		globals()['filename'] = new_file
		break


def wget():
	if not os.path.exists(filename):
		download()
	elif not check_length():
		rename()
		download()
