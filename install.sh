# Creates and loads the launch agent file.

# Timer in minutes. Default 5 minutes.
interval=$((5*60))

# Get username
name=`whoami`

# Set capture folder
dir=$(pwd | sed -e "s/ /\\\ /g")

# plist File
file=~/Library/LaunchAgents/ali.karbassi.nerdstream.plist

# Create the plist file
echo -ne '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n\t<key>Disabled</key>\n\t<false/>\n\t<key>KeepAlive</key>\n\t<false/>\n\t<key>Label</key>\n\t<string>ali.karbassi.nerdstream</string>\n\t<key>ProgramArguments</key>\n\t<array>\n\t\t<string>'$dir'/nerdstream.sh</string>\n\t</array>\n\t<key>QueueDirectories</key>\n\t<array/>\n\t<key>RunAtLoad</key>\n\t<true/>\n\t<key>StartInterval</key>\n\t<integer>'$interval'</integer>\n\t<key>WatchPaths</key>\n\t<array/>\n</dict>\n</plist>' >> $file

# Load the plist file and run it
launchctl load -w $file

