name=ali.karbassi.nerdstream.plist
file=~/Library/LaunchAgents/$name
sudo launchctl stop $file
sudo launchctl unload $file
sudo launchctl remove $name
sudo rm $file
sudo rm -rf .capture
sudo rm capture.sh