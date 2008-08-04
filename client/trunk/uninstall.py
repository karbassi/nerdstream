#!/usr/bin/env python
# encoding: utf-8
"""
uninstall.py

Created by Ali Karbassi on 2008-08-04.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import sys
import os
import shutil
import subprocess

def remove_files():
	files = ['isightcapture', 'nerdstream.py', 'com.sierrabravo.nerdstream.agent.plist',
		'/Users/' + os.getenv('USER') + '/Library/LaunchAgents/com.sierrabravo.nerdstream.agent.plist', 'install.py', 'uninstall.py', 'flickrapi', '/Applications/nerdstream/']
	
	print ''
	print 'Starting to remove files.'
	print '-------------------------'
	for x in files:
		if os.path.exists(x):
			if os.path.isfile(x):
				print 'Removing file: ' + os.path.abspath(x) + ' ...',
				os.remove(x)
				print ' removed.'
			else:
				print 'Removing directory: ' + os.path.abspath(x) + ' ...',
				shutil.rmtree(x)
				print ' removed.'

def stop_process():
	
	print ''
	print 'Starting to remove process.'
	print '-------------------------'
	print 'Rmoving process...',
	
	process = '/Users/' + os.getenv('USER') + '/Library/LaunchAgents/com.sierrabravo.nerdstream.agent.plist'
	subprocess.call('launchctl unload ' + process, shell=True)
	
	print ' removed.'

if __name__ == '__main__':
	if os.getcwd() != sys.argv[0] and os.path.dirname(sys.argv[0]) is not '':
		os.chdir(os.path.dirname(sys.argv[0]))
	
	print ''
	
	if raw_input('NerdStream is about to be uninstalled. Are you sure you want to do this? [Yes/No] ').lower() == 'yes':
		for defs in ['stop_process()', 'remove_files()']:
			try:
				if eval(defs):
					sys.exit()
			except Exception, e:
				print e
		print ''
		print 'All files were removed. Thanks for using NerdStream.'
		print ''
