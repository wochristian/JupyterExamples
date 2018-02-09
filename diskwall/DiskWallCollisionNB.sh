#!/bin/sh
# This script runs the Disk Wall Collision Jupyter Notebook

echo "Run Jupyter notebook."
workdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
nbfile="$workdir/DiskWallCollision.ipynb"
echo "$nbfile"
#jupyter notebook "$nbfile"
/Users/wochristian/anaconda3/bin/jupyter notebook "$nbfile"