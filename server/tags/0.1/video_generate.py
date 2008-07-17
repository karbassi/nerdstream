#!/usr/bin/env python
# encoding: utf-8

import sys, os, glob, shutil, subprocess, time
people = ['akarbass', 'mwoods', 'bdachev', 'minhvu', 'mjohnson']
format = {
			'mp4': {'ext':'mp4', 'b':'350k', 's':'vga', 'r':'10', 'v':'0'}
			}

for p in people:
	shutil.copytree('/home/' + p + '/public_html/nerdstream/', 'temp')
	os.chdir('temp')
	os.remove('latest.jpg')
	d = glob.glob('*.jpg')
	d.sort()
	for i in range(len(d)):
		#newname = '%05d' % (i+1)
		newname = str(i+1)
		newname += '.jpg'
		#print newname
		os.rename(d[i], newname)
	
	# print os.getcwd()
	# sys.exit()
	
	for f in format:
		fileN = p + '.' + format[f]['ext']
		cmd = ['ffmpeg', '-v', format[f]['v'], '-y', '-r', format[f]['r'], '-b', format[f]['b'], '-s', format[f]['s'], '-f', f, '-i', '%d.jpg', fileN]
		subprocess.call(cmd)
		shutil.move(fileN, '../')
	
	os.chdir('../')
	shutil.rmtree('temp')