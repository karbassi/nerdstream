#!/usr/bin/env python
# encoding: utf-8
"""
nerdstream.py

Created by Ali Karbassi on 2008-07-01.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import time, sys, os, shutil, subprocess, threading, ConfigParser, string
from time import strftime
from ftplib import FTP

def createDaemon():
	try:
		pid = os.fork()
		if pid > 0:
			print 'Daemon PID %d' % pid
			print 'Updating every ' + str(config['update every']) + ' minute(s).'
			os._exit(0)
	except OSError, error:
		print 'Failed: %d (%s)' % (error.errno, error.strerror)
		os._exit(1)
	
	# Remove from the parent
	os.setsid()
	os.umask(0)
	
	loop()

def loop():
	while True:
		if int(strftime("%H%M")) > int(config['start time']) and int(strftime("%H%M")) < int(config['end time']):
			if int(strftime("%M")) % config['update every'] == 0:
				take_picture()
				time.sleep(50) # minus one for sake of not matching over previous
			else:
				time.sleep(50) #sleep 50 seconds
		else:
			time.sleep(50) #sleep 50 seconds

def create_latest(file):
	latest_file = config['local dir'] + '/latest.jpg'
	shutil.copy(file, latest_file)
	ftp_image(latest_file)

def take_picture():
	datetime = strftime("%Y%m%dT%H%M")
	filename = config['local dir'] + '/' + datetime + '.jpg'
	subprocess.call("./isightcapture " + filename, shell=True)
	time.sleep(1)
	create_latest(filename)
	ftp_image(filename)

def ftp_image(filename):
	new_dir = os.path.dirname(filename)
	(head, name_of_file) = os.path.split(filename)
	old_dir = os.getcwd()
	os.chdir(new_dir)
	
	# FTP Upload
	ftp = FTP(config['host'])
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

def configuration(file):
	if not os.path.exists(file):
		create_config(file)
	return open_config(file)

def open_config(file):
	fc = ConfigParser.ConfigParser()
	fc.read(file)
	
	c = fc.items("ftp")
	c += fc.items("local")
	c += fc.items("time")
	c += fc.items("information")
	
	nc = {}
	for var in c:
		nc[ var[0] ] = var[1]
	
	# Checking for trailing slash
	if nc['local dir'].endswith("/"):
		nc['local dir'] = nc['local dir'].rstrip("/")
	if nc['ftp dir'].endswith("/"):
		nc['ftp dir'] = nc['ftp dir'].rstrip("/")
	
	# Change timer var from minutes to seconds
	nc['update every'] = int(nc['update every'])
	
	return nc

def create_config(file):
	config = {
				'ftp' : {'host' : 'yankee.sierrabravo.net', 'ftp dir' : 'public_html/nerdstream/', 'username' : '', 'password' : ''},
				'local' : {'local dir' : 'shots/', 'delete local' : 'false'},
				'time' : {'start time' : '0730', 'end time' : '1800', 'update every' : '1'},
				'information' : {'name' : '', 'job title' : ''}
				}
	
	# FTP Information
	config['ftp']['host'] = raw_input("FTP Host ['" + config['ftp']['host'] + "']: ").lower() or config['ftp']['host']
	while config['ftp']['username'] == '': config['ftp']['username'] = raw_input('FTP Username: ') or ''
	while config['ftp']['password'] == '': config['ftp']['password'] = raw_input('FTP Password: ') or ''
	config['ftp']['ftp dir'] = raw_input("FTP Directory ['" + config['ftp']['ftp dir'] + "']: ") or config['ftp']['ftp dir']
	
	# Location Information
	config['local']['local dir'] = raw_input("Local Directory ['" + config['local']['local dir'] + "']: ") or config['local']['local dir']
	config['local']['delete local'] = raw_input("Delete local copy ['" + config['local']['delete local'] + "']: ").lower() or config['local']['delete local']
	
	# Time Information
	config['time']['start time'] = raw_input("Start time ['" + config['time']['start time'] + "']: ") or config['time']['start time']
	config['time']['end time'] = raw_input("End time ['" + config['time']['end time'] + "']: ") or config['time']['end time']
	config['time']['update every'] = raw_input("Update every (in minutes) ['" + config['time']['update every'] + "']: ") or config['time']['update every']
	
	# Personal Information
	while config['information']['name'] == '': config['information']['name'] = raw_input('Full Name: ') or ''
	while config['information']['job title'] == '': config['information']['job title'] = raw_input('Job Title: ') or ''
	
	# Create a ConfigParser to write to a file
	fc = ConfigParser.ConfigParser()
	
	for c in config:
		fc.add_section(c)
		for d in config[c]:
			fc.set(c, d, config[c][d])

	# write to screen
	fc.write(open(file, 'w'))

def __init__(file):
	config = configuration(file)
	if not os.path.exists(config['local dir']):
		os.makedirs(config['local dir'])
	return config

if __name__ == '__main__':
	config = __init__('config.ini')
	createDaemon()