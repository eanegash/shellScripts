#!/bin/bash

# Script will sum the sizes of files that have been changed, in the last 24 hours.
# Results are mailed to root. 
# NEXT: Add script to a cron job

SUM=0
FILES=`find / -mount -type f -mtime -1 | xargs du -k | awk '{print $1}'`

for i in $FILES; do
	SUM=$((SUM+i))
done

SUM=$((SUM/1024))

echo "$SUM MB" | mail -s "$HOSTNAME free space" root
