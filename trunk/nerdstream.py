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
	loop()

def loop():
	while True:
		if int(strftime("%H%M")) > int(config['start time']) and int(strftime("%H%M")) < int(config['end time']):
			if int(strftime("%M")) % (int(config['update every']) / 60) == 0:
				take_picture()
				time.sleep(float(config['update every']) - 1) # minus one for sake of not matching over previous
			else:
				time.sleep(50) #sleep 50 seconds
		else:
			time.sleep(50) #sleep 50 seconds

def take_picture():
	datetime = strftime("%Y%m%dT%H%M")
	filename = config['local dir'] + '/' + datetime + '.jpg'
	subprocess.call("./isightcapture " + filename, shell=True)
	time.sleep(1)
	ftp_image(filename)


def ftp_image(filename):
	new_dir = os.path.dirname(filename)
	(head, name_of_file) = os.path.split(filename)
	old_dir = os.getcwd()
	os.chdir(new_dir)
	
	# FTP Upload
	ftp = FTP("yankee.sierrabravo.net")
	ftp.login(config['username'], config['password'])
	
	for directory in config['ftp dir'].split('/'):
		try:
			ftp.cwd(directory)
		except Exception, e:
			ftp.mkd(directory)
			ftp.cwd(directory)
	
	fi = open(name_of_file, "rb")
	ftp.storbinary("STOR " + name_of_file, fi, 1)
	ftp.quit()
	
	# Remove file
	if config['delete local'].lower() == 'true':
		os.remove(name_of_file)
	
	# Move back to old dir so the script will continue to run
	os.chdir(old_dir)

def open_config(file):
	if not os.path.exists(file):
		print "'" + file + ".ini' file does not exist. Copy over '" + file + "-dist'."
		sys.exit();
	
	c = ConfigParser.ConfigParser()
	c.read(file)
	
	config = c.items("ftp")
	config += c.items("local")
	config += c.items("time")
	config += c.items("information")
	
	nc = {}
	for var in config:
		if var[1] == '':
			print 'Please fill out config.ini'
			sys.exit()
		nc[ var[0] ] = var[1]
	
	# Checking for trailing slash
	if nc['local dir'].endswith("/"):
		nc['local dir'] = nc['local dir'].rstrip("/")
	if nc['ftp dir'].endswith("/"):
		nc['ftp dir'] = nc['ftp dir'].rstrip("/")

	
	return nc

if __name__ == '__main__':
	config = open_config('config.ini')
	
	if not os.path.exists(config['local dir']):
		os.makedirs(config['local dir'])
	createDaemon()