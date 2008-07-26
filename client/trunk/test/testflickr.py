import sys
import os
import subprocess
from flickrapi import FlickrAPI

api_key = 'ad176a252ba707a54af27cbdd35c5760'
user_id = '28598515@N02'
secret_key='2e9f114458f5889e'

flickr = FlickrAPI(api_key,secret_key, format='etree')

#authenticate
# (token, frob) = flickr.get_token_part_one(perms='write')
# if not token:
# 	raw_input("Press ENTER after you authorized this program")
# flickr.get_token_part_two((token, frob))

# # Get Login information
# ret = flickr.test_login(api_key=api_key)
# for i in ret:
# 	print i.attrib['id'] == user_id

# the call back function
def func(progress, done):
	if done:
		print "done"
	else:
		print "at %s%%" % progress

#the upload function, change the filename, and tag, or if want it to be private, change is_public=1 to is_public=0
subprocess.call("./isightcapture -t png test.png", shell=True)
rsp = flickr.upload(filename="test.png",
	callback=func,
	title='Ali Karbassi',
	description = 'Testing Upload feature.',
	tags='NerdStream ns:user="Ali Karbassi" ns:title="Programmer"',
	is_public='0',
	is_friend='1',
	is_family='0',
	safety_level='1',
	content_type='1',
	hidden='1'
	)