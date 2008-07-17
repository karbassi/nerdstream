#!/usr/bin/env python
import os
import signal

# Change this to your process name
processname = 'nerdstream'

for line in os.popen("ps ax"):
	fields = line.split()
	pid = fields[0]
	process = fields[4]
	
	# print fields[4]
	
	if process.find(processname) > 0:
		# Kill the Process. Change signal.SIGHUP to signal.SIGKILL if you like
		print int(pid) # + signal.SIGHUP
		# break