#!/bin/bash

find -name *.bin>loc_data.txt
cat loc_data.txt|while read line; 
do

echo ${line:2}
if [ -z "$line" ]
then
      echo "\$line is empty"
else
    CloudCompare -SILENT -C_EXPORT_FMT ASC -PREC 12 -SEP SPACE -EXT txt -LOG_FILE ${line:11:-4}.txt -O ${line:2} -SS SPATIAL 0.000000001   
    python3 util.py -file=${line:11:-4}
fi

done
