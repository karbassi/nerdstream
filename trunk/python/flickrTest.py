#!/usr/bin/env python
# encoding: utf-8
"""
flickrTest.py

Created by Ali Karbassi on 2008-07-13.
Copyright (c) 2008 Ali Karbassi. All rights reserved.
"""

import sys
import os
from flickrapi import FlickrAPI

api_key = 'ad176a252ba707a54af27cbdd35c5760'
user_id = '28598515@N02'
secret_key='2e9f114458f5889e'

flickr = FlickrAPI(api_key,secret_key, format='etree')

#authenticate
(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
	raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

# # the call back function
# def func(progress, done):
# 	if done:
# 		print "done"
# 	else:
# 		print "at %s%%" % progress
# 
# #the upload function, change the filename, and tag, or if want it to be private, change is_public=1 to is_public=0
# rsp = flickr.upload(filename="/Users/akarbass/Desktop/_glasses.jpg",
# 	callback=func,
# 	title='Ali Karbassi',
# 	description = 'Testing Upload feature.',
# 	tags='NerdStream ns:user="Ali Karbassi" ns:title="Programmer"',
# 	is_public='0',
# 	is_friend='1',
# 	is_family='0',
# 	safety_level='1',
# 	content_type='1',
# 	hidden='1'
# 	)
# photo_id = rsp.photoid[0].text
# print flickr.photosets_create(api_key=api_key, title="Hello", primary_photo_id=photo_id).text

# # GET PHOTOSETS
# ret = flickr.photosets_getList(api_key=api_key)
# 
# for i in ret.find('photosets').findall('photoset'):
# 	title = i.find('title').text
# 	id = i.attrib['id']
# 	if 'Event' in title and not 'Private' in title:
# 		print id + " : " + title

ret = flickr.tags_getListUserRaw(api_key=api_key)

for i in ret.find('who').find('tags').findall('tag'):
	print i.attrib['clean']
	r2 = flickr.photos_search(api_key=api_key, user_id=user_id, tags=i.attrib['clean'] + ',ns:')
	for j in r2.find('photos').findall('photo'):
		print j.attrib
	


