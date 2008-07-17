#
#  controller.py
#  QuickTag
#
#  Created by Scott Paul Robertson on 6/11/08.
#  Copyright (c) 2008 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *

class controller(NSWindowController):
	fullName = IBOutlet()
	jobTitle = IBOutlet()
	ftpHost = IBOutlet()
	ftpUsername = IBOutlet()
	ftpPassword = IBOutlet()
	updateEvery = IBOutlet()
	localDirectory = IBOutlet()
	
	def awakeFromNib(self):
		print "open"

#	@IBAction
#	def save_(self, sender):
#		print "save"

#	@IBAction
#	def open_(self, sender):
#		print "open"

	@IBAction
	def revert_(self, sender):
		self.fullName.setStringValue_("Ali Karbassi")
		print "revert"

#	@IBAction
#	def saveClose_(self, sender):
#		print "Save & Close"
#		self.save_(sender)
#		print "Close?"

#	@IBAction
#	def updateField_(self, sender):
#		print sender.description()
#		print self.name.description()
#		print "Updating Field: " + sender.stringValue()