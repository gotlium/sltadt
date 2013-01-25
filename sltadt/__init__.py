# -*- coding: utf-8 -*-


__author__ = 'GoTLiuM InSPiRIT <gotlium@gmail.com>'


import os
import re
import time
import atexit
import argparse
import urlparse


START_HTTPRY = "sudo httpry -d -i %s -t 1 -f 'host,request-uri' -o '%s' %s " \
			   " 2> /dev/null"
STOP_HTTPRY = 'sudo killall -9 httpry >& /dev/null'
WGET_BIN = "wget_in_bg '%s'"
ALLOWED_EXT = ['.flv', '.mp4', '.mp3']
VERSION = (1,0)


def exit_function():
	os.system(STOP_HTTPRY)


def tailf(file):
	interval = 1.0

	while True:
		where = file.tell()
		line = file.readline()
		if not line:
			time.sleep(interval)
			file.seek(where)
		else:
			yield line


def run():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--interface')
	parser.add_argument('-e', '--ext')
	parser.add_argument('-p', '--port')
	parser.add_argument('-r', '--regexp')
	args = parser.parse_args()

	interface = args.interface if args.interface else 'en1'
	allowed_ext = args.ext if args.ext else ALLOWED_EXT
	port = "'tcp dst port %s'" % args.port if args.port else ''
	regexp = args.regexp
	pwd = os.getcwd()
	log = "%s/httpry.log" % pwd

	atexit.register(exit_function)

	os.system('clear')
	os.system(STOP_HTTPRY)
	time.sleep(1)
	if os.path.exists(log):
		os.unlink(log)
	os.system(START_HTTPRY % (interface, log, port))
	os.chdir(pwd)

	print "Listening on %s ..." % interface
	stored = []
	for line in tailf(open(log)):
		if not line:
			continue
		line = ''.join(line.strip().split('\t'))
		path = urlparse.urlparse(line).path
		filename = os.path.basename(path)
		ext = os.path.splitext(filename)[1].strip()
		if len(ext) > 2 and ext in allowed_ext:
			if regexp and not re.match(regexp, line):
				continue
			url = 'http://%s' % line
			if url not in stored:
				os.system(WGET_BIN % url)
				stored.append(url)
				print '> url: %s, ext: %s' % (url, ext)
