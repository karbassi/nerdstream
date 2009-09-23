#!/bin/bash

# Get username
name=`whoami`

# Set capture folder
dir=`pwd`'/capture/'

# Create capture folder if it doesn't exist
if [[ ! -d "$dir" ]]; then
    mkdir -p $dir
fi

# Set file name
file=$dir"`date +%Y-%m-%d_%H-%M-%S`.jpg"

# Take the picture
`pwd`'/isightcapture' $file

# Upload file
curl -F "img=@$file;type=image/jpeg" -F "name=$name" http://ali.karbassi.com/isight/test.php

# Remove the file after upload
rm $file