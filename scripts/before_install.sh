#!/bin/bash

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid1=$(echo ${var} | cut -d " " -f2)
pid2=$(echo ${var} | cut -d " " -f16)
if [ -n "${pid}" ]
then 
    sudo kill -9 ${pid1}
    sudo kill -9 ${pid2}
    echo ${pid1} is terminated.
else
    echo ${pid1} is not running.
fi

rm -rf /home/ubuntu/recipe_BE
mkdir  /home/ubuntu/recipe_BE
