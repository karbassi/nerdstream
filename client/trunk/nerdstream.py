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
import urllib2
import webbrowser
from time import strftime
from ConfigParser import ConfigParser

from flickrapi import FlickrAPI

def loop():
	if config['last_update'] != datetime:
		if int(strftime("%H%M")) > int(config['start_time']) and int(strftime("%H%M")) < int(config['end_time']):
			if int(strftime('%M')) % int(config['interval']) is 0:
				take_picture()

def take_picture():
	# filename = config['local_dir'] + '/' + datetime + '.png'
	filename = './' + datetime + '.png'
	subprocess.call("./isightcapture -t png " + filename, shell=True)
	time.sleep(1)
	upload_to_flickr(filename, date)
	update_time()
	del_file(filename)

def update_time():
	# print urllib2.urlopen(base_url + '/user/' + os.getenv('USER') + '/update/').read()
	pass
	
def del_file(filename):
	os.remove(filename)

def upload_to_flickr(filename, tags):
	api_key = 'ad176a252ba707a54af27cbdd35c5760'
	user_id = '48251447@N00'
	secret_key='2e9f114458f5889e'
	
	flickr = FlickrAPI(api_key,secret_key, format='etree')
	
	(token, frob) = flickr.get_token_part_one(perms='write')
	
	if not token:
		raw_input("Press ENTER after you authorized this program")
	
	flickr.get_token_part_two((token, frob))
	
	# Start off the tag list
	t = ''
	
	#Create tag list
	for x in tags:
		t += '"ns:' + x + '=' + tags[x] + '" '
	
	t += '"ns:user=' + config['full name'] + '" '
	t += '"ns:title=' + config['job_title'] + '" '
	
	#the upload function, change the filename, and tag, or if want it to be private, change is_public=1 to is_public=0
	rsp = flickr.upload(filename=filename,
		# callback=func,
		title=config['full name'] + ' @ ' + tags['hour'] + ':' + tags['minute'],
		# description = 'Testing Upload feature.',
		tags='NerdStream ' + t,
		is_public='0',
		is_friend='1',
		is_family='0',
		safety_level='1',
		content_type='1',
		hidden='1'
		)
	
	# photo_id = rsp.photoid[0].text

def configuration():
	global config
	config = eval(urllib2.urlopen(base_url + '/user/' + os.getenv('USER') + '/config/').read())
	if config['full name'] == '':
		raw_input("You are not part of the nerdstream system. Press enter to go sign up. When you're done, come back here.")
		webbrowser.open(base_url + '/create/' + os.getenv('USER'))
		raw_input("Press ENTER after you signed up.")
		configuration()

def __init__():
	if os.getcwd() != sys.argv[0] and os.path.dirname(sys.argv[0]) is not '':
		os.chdir(os.path.dirname(sys.argv[0]))
	
	configuration()
	
	# if not os.path.exists(config['local_dir']):
		# os.makedirs(config['local_dir'])
	
	global date, datetime
	
	date = {
		'year':strftime('%Y'),
		'month':strftime('%m'),
		'day':strftime('%d'),
		'hour':strftime('%H'),
		'minute':strftime('%M'),
		'second':strftime('%S'),
		'weekday':strftime('%A')}
	
	datetime = date['year'] + date['month'] + date['day'] + 'T' + date['hour'] + date['minute']

if __name__ == '__main__':
	base_url = 'http://nerdstream.appspot.com'
	__init__()
	loop()