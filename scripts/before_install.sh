#!/bin/bash

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid1=$(echo "${var}" | awk '{print $2}')
pid2=$(echo "${var}" | awk '{print $16}')

if [ -n "${pid1}" ] && [ -n "${pid2}" ]; then
    sudo kill -9 "${pid1}"
    sudo kill -9 "${pid2}"
    echo "${pid1} and ${pid2} are terminated."
else
    echo "gunicorn processes are not running."
fi

# rm -rf /home/ubuntu/gunicorn.log

rm -rf /home/ubuntu/recipe_BE
mkdir  /home/ubuntu/recipe_BE
