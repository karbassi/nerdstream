#!/usr/bin/env python
# encoding: utf-8
"""
nerdstream.py

Created by Ali Karbassi on 2008-07-01.
Updated: 2008-08-04
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import sys
import os
import string
import time
import shutil
import subprocess
import urllib2
import webbrowser
from time import strftime

from flickrapi import FlickrAPI

def loop():
	# Check to make the weekdate is between Monday and Friday (work week) and
	# Make sure the time is between the servers start and end time and
	# Make sure a picture is taken only once per minute and
	# Make sure the time is an interval of the server's interval. Every x minutes.
	if weekday is not 0 and weekday is not 6 and \
		current_time > int(config['start_time']) and current_time < int(config['end_time']) and \
		last_update != datetime and \
		int(strftime('%M')) % int(config['interval']) is 0:
			
			# Take the picture and return the image file name
			take_picture()
			
			# Sleep for 1 second for the camera to finish taking the picture. This is a good thing to have because sometimes the camera lags.
			time.sleep(1)
			
			# Upload the image to flickr
			upload_to_flickr(date)
			
			# After the picture has been uploaded, update the picture time
			update_time()
			
			# Delete the local file
			os.remove(filename)

def take_picture():
	"""Call program to take the picture"""
	subprocess.call('./isightcapture -t png ' + filename, shell=True)

def update_time():
	"""Call the server page to update the late update time"""
	urllib2.urlopen(base_url + '/config/' + computer_name + '/update/').read()

def upload_to_flickr(tags):
	
	# Start off the tag list
	t = ''
	
	# Create tag list
	for x in tags:
		t += '"ns:' + x + '=' + tags[x] + '" '
	
	t += '"ns:user=' + config['full name'] + '" '
	t += '"ns:title=' + config['job_title'] + '" '
	
	#t he upload function, change the filename, and tag, or if want it to be private, change is_public=1 to is_public=0
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

def get_config():
	global config
	config = eval(urllib2.urlopen(base_url + '/config/' + computer_name + '/').read())
	
	if config['full name'] == '':
		raw_input("You are not part of the nerdstream system. Press enter to go sign up. When you're done, come back here.")
		webbrowser.open(base_url + '/create/' + computer_name)
		raw_input("Press ENTER after you signed up.")
		get_config()

def check_flickr():
	"""Make sure the computer is registered with flickr"""
	
	global flickr, token, frob
	flickr = FlickrAPI(api_key, secret_key, format='etree')
	(token, frob) = flickr.get_token_part_one(perms='write')
	
	if not token:
		raw_input("Press ENTER after you authorized this program")
		flickr.get_token_part_two((token, frob))
		check_flickr()

def __init__():
	# if not os.path.exists(config['local_dir']):
		# os.makedirs(config['local_dir'])
	
	global date, datetime, weekday, current_time, last_update, filename, computer_name
	
	# Walk to the location of this file. This makes sure the files being called, the isightcapture, work correctly.
	if os.getcwd() != sys.argv[0] and os.path.dirname(sys.argv[0]) is not '':
		os.chdir(os.path.dirname(sys.argv[0]))
	
	# The user's computer name. Currently works only on *nix based systems.
	computer_name = os.getenv('USER')
	
	# Get the configuration items.
	get_config()
	
	# Make sure the user is authorized with flickr.
	check_flickr()
	
	date = {
		'year':strftime('%Y'),
		'month':strftime('%m'),
		'day':strftime('%d'),
		'hour':strftime('%H'),
		'minute':strftime('%M'),
		'second':strftime('%S'),
		'weekday':strftime('%A')
	}
	
	# Time difference between localhost and google appengine
	# server_diff = 5
	
	# Datetime formed. YYYY-MM-DD HH:MM
	# datetime = date['year'] + '-' + date['month'] + '-' + date['day'] + ' ' + str(int(date['hour']) + server_diff) + ':' + date['minute']
	
	# Chop off the seconds from the update field.
	# last_update = config['last_update'][0:16]
	
	# Changed to minute because the program needs to check if the image was updated in the span of the same minute
	last_update = config['last_update'][14:16]
	datetime = date['minute']
	
	# Get the current weekday (0 - sunday, 1 - monday, ..., 6 - saturday)
	weekday = int(strftime('%w'))
	
	# Get the current time in HHMM form
	current_time = int(strftime("%H%M"))
	
	# File name is real fun here. It will produce the following: "FullName-YYYYMMDDTHHMM.png"
	filename = './' + ''.join(c for c in config['full name'] if not c.isspace()) + "-" + date['year'] + date['month'] + date['day'] + 'T' + date['hour'] + date['minute'] + '.png'

if __name__ == '__main__':
	api_key = 'ad176a252ba707a54af27cbdd35c5760'
	secret_key='2e9f114458f5889e'
	base_url = 'http://nerdstream.appspot.com'
	__init__()
	loop()