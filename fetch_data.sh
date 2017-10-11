#!/bin/bash

cd /Users/david/CloudStation/Coding/mbta_visualizer

COUNTER=0

while [ $COUNTER -lt 2880 ]; 
	do python mv_fetch_data.py;
	echo the loop is $COUNTER;
	sleep 30;
	let COUNTER=COUNTER+1;
done;
