# Creates and loads the launch agent file.

# Timer in minutes. Default 5 minutes.
interval=$((5*60))

# Need to install with root access
if [[ `whoami` != "root" ]]; then
    echo "Please call with root access."
    exit
fi

# Get username
if [[ -z $1 ]]; then
    echo "Usage: $0 username"
    echo "Example: $0 ali"
    exit
fi

# Set username
name=$1

# Set capture folder
dir=$(pwd | sed -e "s/ /\\\ /g")

# Set up the capture file with the pwd
tmp=$(echo $dir | sed "s/\//\\\\\//g")
sed s/\#cur_pwd=/cur_pwd=\"$tmp\"/ <$dir'/nerdstream.sh' > $dir'/_capture.sh'

# Set the username
sed s/\#username=/username=\"$name\"/ <$dir'/_capture.sh' > $dir'/capture.sh'
rm $dir'/_capture.sh'

# Set permissions
chmod 777 capture.sh
chmod 777 isightcapture
chown root isightcapture
chmod 777 uninstall.sh


# plist File
file=~/Library/LaunchAgents/ali.karbassi.nerdstream.plist

# Create the plist file
echo '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n\t<key>Disabled</key>\n\t<false/>\n\t<key>KeepAlive</key>\n\t<false/>\n\t<key>Label</key>\n\t<string>ali.karbassi.nerdstream</string>\n\t<key>ProgramArguments</key>\n\t<array>\n\t\t<string>'$dir'/capture.sh</string>\n\t</array>\n\t<key>QueueDirectories</key>\n\t<array/>\n\t<key>RunAtLoad</key>\n\t<true/>\n\t<key>StartInterval</key>\n\t<integer>'$interval'</integer>\n\t<key>WatchPaths</key>\n\t<array/>\n</dict>\n</plist>' > $file

# Load the plist file and run it
launchctl load $file