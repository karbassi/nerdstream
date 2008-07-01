#!/usr/bin/env python
# encoding: utf-8
"""
nerdstream.py

Created by Ali Karbassi on 2008-07-01.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import time, sys, os, subprocess, threading, ConfigParser, string
from time import strftime
from ftplib import FTP

def createDaemon():
	try:
		pid = os.fork()
		if pid > 0:
			print 'Daemon PID %d' % pid
			os._exit(0)
	except OSError, error:
		print 'fork #2 failed: %d (%s)' % (error.errno, error.strerror)
		os._exit(1)
	take_picture(5)

def take_picture(sleep_time):
	while True:
		if int(strftime("%M")) % 5 == 0:
			datetime = strftime("%Y%m%dT%H%M")
			filename = username + '/' + datetime + '.jpg'
			subprocess.call("./isightcapture " + filename, shell=True)
			time.sleep(1)
			ftp_image(filename)
			time.sleep(sleep_time)
		else:
			time.sleep(30)

def ftp_image(filename):
	new_dir = os.path.dirname(filename)
	(head, name_of_file) = os.path.split(filename)
	old_dir = os.getcwd()
	os.chdir(new_dir)

	# FTP Upload
	ftp = FTP("yankee.sierrabravo.net")
	ftp.login(ftp_user, ftp_pass)
	ftp.cwd('public_html')
	fi = open(name_of_file, "rb")
	ftp.storbinary("STOR " + name_of_file, fi, 1)
	ftp.quit()
	
	# Remove file
	os.remove(name_of_file)
	
	# Move back to old dir so the script will continue to run
	os.chdir(old_dir)

def open_config():
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	ftp_user = config.get("ftp", "username")
	ftp_pass = config.get("ftp", "password")
	if ftp_user == '' or ftp_pass == '':
		print 'Please fill out config.ini'
		sys.exit()
	else:
		return (ftp_user, ftp_pass)

if __name__ == '__main__':
	username = os.environ.get("LOGNAME",'')
	(ftp_user, ftp_pass) = open_config()
	if not os.path.exists(username):
		os.mkdir(username)
	createDaemon()