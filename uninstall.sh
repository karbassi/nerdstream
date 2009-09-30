file=~/Library/LaunchAgents/ali.karbassi.nerdstream.plist
sudo launchctl unload $file
sudo rm $file
sudo rm -rf .capture
sudo rm capture.sh