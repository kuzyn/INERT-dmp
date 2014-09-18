#!/bin/bash
logfile=/home/odroid/bin/dmp/log_fmonitor.log
path=$1
file=$2
fullfilepath="$path/$file"
fullfilemime=`file -b --mime-type ${fullfilepath}`
mime=${fullfilemime%/*}
filetmp="/var/tmp/${file}"
playerdir="/var/www/dmp/player"
datetime=`date --rfc-3339=ns`

echo "${datetime} File created " ${fullfilepath} >> ${logfile}

if [ ${mime} == "image" ]
then
 	echo "${datetime} File ${file}  is an image" >> ${logfile}
 	mv ${fullfilepath} ${filetmp}
	if [[ ${file: 4} != ".gif" ]]
	then
 	echo "${datetime} File moved to ${filetmp}" >> ${logfile} 
 	ffmpeg -loop 1 -i ${filetmp} -c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -t 10  ${filetmp}.mp4
	echo "${datetime} File ${filetmp}.mp4  converted" >> ${logfile}	
	mv ${filetmp}.mp4 "${playerdir}/${datetime}".mp4
	rm ${filetmp}
	fi
fi

if [ ${mime} == "video" ]
then
 	echo "${datetime} File ${file}  is a video" >> ${logfile}
	mv ${fullfilepath} "${playerdir}/${datetime}-${file}"
fi
