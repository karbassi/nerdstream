#!/usr/bin/env python
# encoding: utf-8
"""
install.py

Created by Ali Karbassi on 2008-08-04.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import sys
import os
import shutil
import subprocess
import urllib2
import webbrowser

from flickrapi import FlickrAPI

def check_server():
	base_url = 'http://nerdstream.appspot.com'
	computer_name =  os.getenv('USER')
	config = eval(urllib2.urlopen(base_url + '/config/' + computer_name + '/').read())
	
	if config['full name'] == '':
		print ''
		raw_input("You are not part of the nerdstream system. Press enter to go sign up. When you're done, come back here.")
		webbrowser.open(base_url + '/create/' + computer_name)
		print ''
		raw_input("Press ENTER after you signed up.")
		check_server()
		
def check_flickr():
	"""Make sure the computer is registered with flickr"""
	api_key = 'ad176a252ba707a54af27cbdd35c5760'
	secret_key='2e9f114458f5889e'
	flickr = FlickrAPI(api_key, secret_key, format='etree')
	(token, frob) = flickr.get_token_part_one(perms='write')
	
	if not token:
		raw_input("Press ENTER after you authorized this program")
		flickr.get_token_part_two((token, frob))
		check_flickr()

def check_files():
	"""Check to see if all the files were included"""
	files = ['isightcapture', 'nerdstream.py', 'flickrapi', 'com.sierrabravo.nerdstream.agent.plist', 'install.py', 'uninstall.py']
	fail = False
	for x in files:
		if not os.path.exists(x):
			fail = True
			print x + " doesn't exist."
	
	return fail

def create_process():
	
	process_dir = '/Users/' + os.getenv('USER') + '/Library/LaunchAgents'
	
	if not os.path.exists(process_dir):
		os.makedirs(process_dir)
	
	file_from = 'com.sierrabravo.nerdstream.agent.plist'
	file_to = process_dir + '/' + file_from
	
	shutil.move(file_from, file_to)
	
	subprocess.call('launchctl load ' + file_to, shell=True)

def make_executable():
	files = ['isightcapture', 'nerdstream.py', 'install.py', 'uninstall.py']
	for x in files:
		if os.path.exists(x):
			os.chmod(x, 0755)


if __name__ == '__main__':
	if os.getcwd() != sys.argv[0] and os.path.dirname(sys.argv[0]) is not '':
		os.chdir(os.path.dirname(sys.argv[0]))
	
	for defs in ['check_files()', 'check_server()', 'check_flickr()', 'make_executable()', 'create_process()']:
		try:
			if eval(defs):
				sys.exit()
		except Exception, e:
			print e
	
	print ''
	print 'NerdStream has been installed. Please do not delete the files yourself. Use the uninstall.py script.'
	print ''
