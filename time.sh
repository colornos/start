#!/bin/bash

while true;
do
    DATE=`date | cut -d' ' -f4`
    echo $DATE
    if [[ $DATE == "11:33:00" ]]
    then
            echo "this is a test program"
            sleep 1s
    fi
done
