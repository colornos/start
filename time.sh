#! /bin/bash

RUNAT="07:54"

while [ 1 ]
do
    DATE=`/bin/date +%H:%M`
    if [ $DATE. = $RUNAT. ]
    then
        echo "Hello world"
    fi

    sleep 60
done
