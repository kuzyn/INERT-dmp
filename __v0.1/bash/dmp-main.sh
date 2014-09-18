#! /bin/bash
BASEPATH=/var/www/dmp/player
FILES=$BASEPATH/*
shopt -s nullglob
while :
do
	for f in $FILES
	do
  	ffplay -t 5 -an -fs -autoexit "$f"
	sleep 1
	done
done 
