#
#  NerdStreamAppDelegate.py
#  NerdStream
#
#  Created by Ali Karbassi on 7/3/08.
#  Copyright __MyCompanyName__ 2008. All rights reserved.
#

from Foundation import *
from AppKit import *

class NerdStreamAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
