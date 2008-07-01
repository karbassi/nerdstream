#!/usr/bin/env python
# encoding: utf-8
"""
dailyCapture.py

Created by Ali Karbassi on 2008-07-01.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import time, sys, os, subprocess, threading
from time import strftime

def createDaemon():
	try:
		pid = os.fork()
		if pid > 0:
			print 'Daemon PID %d' % pid
			os._exit(0)
	except OSError, error:
		print 'fork #2 failed: %d (%s)' % (error.errno, error.strerror)
		os._exit(1)

	take_picture(300) # function demo
	
def take_picture(sleep_time):
	import time

	while True:
		if int(strftime("%M")) % 5 == 0:
			datetime = strftime("%Y%m%dT%H%M%S")
			filename = username + "-" + datetime
			subprocess.call("./isightcapture -n 10 " + username + "/" + filename + ".jpg", shell=True)
			time.sleep(sleep_time)
		else:
			time.sleep(30)
	
if __name__ == '__main__':
	username = os.environ.get("LOGNAME",'')
	if not os.path.exists(username):
		os.mkdir(username)
	createDaemon()