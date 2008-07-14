#!/usr/bin/env python
# encoding: utf-8
"""
nerdstream.py

Created by Ali Karbassi on 2008-07-01.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import sys
import os
import string
import time
import shutil
import subprocess
import threading
from ConfigParser import ConfigParser
from time import strftime

from flickrapi import FlickrAPI

def loop():
	if int(strftime("%H%M")) > int(config['start time']) and int(strftime("%H%M")) < int(config['end time']):
		print int(strftime("%H%M"))
		print int(config['start time'])
		print int(strftime("%H%M"))
		print int(config['end time'])
		take_picture()

# def create_latest(file):
# 	latest_file = config['local dir'] + '/latest.jpg'
# 	shutil.copy(file, latest_file)
# 	upload_to_flickr(latest_file)

def take_picture():
	datetime = strftime("%Y%m%dT%H%M")
	filename = config['local dir'] + '/' + datetime + '.jpg'
	subprocess.call("./isightcapture " + filename, shell=True)
	time.sleep(1)
	# create_latest(filename)
	upload_to_flickr(filename)

def upload_to_flickr(filename):
	api_key = 'ad176a252ba707a54af27cbdd35c5760'
	user_id = '48251447@N00'
	secret_key='2e9f114458f5889e'
	
	flickr = FlickrAPI(api_key,secret_key, format='etree')
	
	(token, frob) = flickr.get_token_part_one(perms='write')
	
	if not token:
		raw_input("Press ENTER after you authorized this program")
		
	flickr.get_token_part_two((token, frob))
	
	#the upload function, change the filename, and tag, or if want it to be private, change is_public=1 to is_public=0
	rsp = flickr.upload(filename=filename,
		# callback=func,
		title=config['name'] + ' @ ' + strftime("%Y%m%dT%H%M"),
		# description = 'Testing Upload feature.',
		tags='NerdStream ns:user="' + config['name'] + '" ns:title="' + config['job title'] + '"',
		is_public='0',
		is_friend='0',
		is_family='0',
		safety_level='1',
		content_type='1',
		hidden='1'
		)
	# photo_id = rsp.photoid[0].text


def configuration(file):
	if not os.path.exists(file):
		create_config(file)
	return open_config(file)

def open_config(file):
	fc = ConfigParser()
	fc.read(file)
	
	c = fc.items("local")
	c += fc.items("time")
	c += fc.items("information")
	
	nc = {}
	for var in c:
		nc[ var[0] ] = var[1]
	
	# Checking for trailing slash
	if nc['local dir'].endswith("/"):
		nc['local dir'] = nc['local dir'].rstrip("/")
	
	# Change timer var from minutes to seconds
	nc['update every'] = int(nc['update every'])
	
	return nc

def create_config(file):
	config = {
		'local' : {'local dir' : 'shots/', 'delete local' : 'false'},
		'time' : {'start time' : '0730', 'end time' : '1800', 'update every' : '1'},
		'information' : {'name' : '', 'job title' : ''}
	}
	
	# Location Information
	config['local']['local dir'] = raw_input("Local Directory ['" + config['local']['local dir'] + "']: ") or config['local']['local dir']
	config['local']['delete local'] = raw_input("Delete local copy ['" + config['local']['delete local'] + "']: ").lower() or config['local']['delete local']
	
	# Time Information
	config['time']['start time'] = raw_input("Start time ['" + config['time']['start time'] + "']: ") or config['time']['start time']
	config['time']['end time'] = raw_input("End time ['" + config['time']['end time'] + "']: ") or config['time']['end time']
	config['time']['update every'] = raw_input("Update every (in minutes) ['" + config['time']['update every'] + "']: ") or config['time']['update every']
	
	# Personal Information
	while config['information']['name'] == '':
		config['information']['name'] = raw_input('Full Name: ') or ''
	while config['information']['job title'] == '':
		config['information']['job title'] = raw_input('Job Title: ') or ''
	
	# Create a ConfigParser to write to a file
	fc = ConfigParser.ConfigParser()
	
	for c in config:
		fc.add_section(c)
		for d in config[c]:
			fc.set(c, d, config[c][d])

	# write to screen
	fc.write(open(file, 'w'))

def __init__(file):
	if os.getcwd() != sys.argv[0] and os.path.dirname(sys.argv[0]) is not '':
		os.chdir(os.path.dirname(sys.argv[0]))
	config = configuration(file)
	if not os.path.exists(config['local dir']):
		os.makedirs(config['local dir'])
	return config

if __name__ == '__main__':
	# print sys.argv
	# print os.getcwd()
	# print os.path.dirname(sys.argv[0])
	config = __init__('config.ini')
	# print config
	loop()
