#!/bin/bash
# Tool to measure root disk space. Returns Used adn Available space on network

TOTAL=0
USED=0
OUT=""

#Create an array of the machines that will be accessed for measurement

MACHINES=()


# Loop through the array, SSM to each machine and run df /.
# We want to ommit the header line of the output so we use tail... 
# - is used as a delimiter. So that we can parse the output with cut command

for m in "${MACHINES[@]}" 
	do
		OUT="$OUT~`ssh $m 'df / | tail -n +2'`"
	done

# Calculate the number of machines in the array.
LENGHTH=${#MACHINES[@]}
LENGTH=$((LENGTH + 1))

# Loop throught the output of df. Start at 2. 
# Parse the output to get the total and available sizes
for (( i=2; i<$LENGTH; i++ ))
	do
		USED_TEMP=`echo $OUT | cut -d "~" -f $i | cut -d " " -f 3`
		TOTAL_TEMP`echo $OUT | cut -d "~" -f $i | cut -d " " -f 2`
		USED=$((USED+USED_TEMP))
		TOTAL=$((TOTAL+TOTAL_TEMP))
	done

# Convert to GB
TOTAL=$((TOTAL/1024/1024))
USED=$((USED/1024/1024))
echo "TOTAL: " $TOTAL "GB"
echo "USED: " $USED "GB"
