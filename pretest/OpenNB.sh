#!/bin/sh
# This script runs the Disk Wall Collision Jupyter Notebook
workdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$workdir"
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    read -e -p "Enter the files you would like to install: " nbfile
fi
echo "Run Jupyter notebook. $arg1"

#nbfile="$workdir/DiskWallCollision.ipynb"
echo "$nbfile"
#jupyter notebook "$nbfile"
if [ -e /Users/wochristian/anaconda/bin/jupyter ]
then
    /Users/wochristian/anaconda/bin/jupyter notebook "$nbfile"
else
    /Users/wochristian/anaconda3/bin/jupyter notebook "$nbfile"
fi

/Users/wochristian/anaconda3/bin/jupyter notebook "$nbfile"
