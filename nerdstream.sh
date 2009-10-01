#!/bin/bash

# Get username
#username=

# Where the script is located
#cur_pwd=

if [[ -z $username ]] || [[ -z $cur_pwd ]]; then
    exit
fi

cwd=$(echo $cur_pwd | sed -e "s/ /\\\ /g")

# Set capture folder
dir=$cwd'/.capture/'

# Create capture folder if it doesn't exist
if [[ ! -d "$dir" ]]; then
    mkdir -p $dir
    chmod -R 755 $dir
fi

# Set file name
file=$dir"`date +%Y-%m-%d_%H-%M-%S`.jpg"

# Take the picture
capture=$cwd'/isightcapture'
$capture $file

# Server Settings
server="ali.karbassi.com"
serverfile="http://"$server"/isight/test.php"

# Check to see if server is up
x=`ping -c1 $server 2>&1 | grep -i unknown`

# If it is, upload all the images in the capture folder, and delete them.
# If not, leave the files in there for when the server comes back online.
if [ "$x" = "" ]; then
    imgs=$dir"*"
    for f in `ls $imgs`
    do
        # Escape spaces
        f=$(echo $f | sed -e "s/ /\\\ /g")

        tags=$(echo 'tags: Nerdstream ns:year='`date +%Y`' ns:month='`date +%m`' ns:weekday='`date +%u`' ns:day='`date +%m`' ns:hour='`date +%H`' ns:minute='`date +%M`' ns:second='`date +%S`' ns:user='$username | sed -e "s/:/%3A/g" | sed -e "s/ /%20/g" | sed -e "s/=/%3D/g" )
        
        title=$(echo $username' @ '`date +"%H:%M"` | sed -e "s/:/%3A/g" | sed -e "s/ /%20/g" | sed -e "s/=/%3D/g" )
        
        # Upload file
        curl -s -F "img=@$f;type=image/jpeg" \
           -F "name=$username" \
           -F "title="$title \
           -F "description="$tags \
           $serverfile

        # Remove the file after upload
        rm $f
    done
fi
