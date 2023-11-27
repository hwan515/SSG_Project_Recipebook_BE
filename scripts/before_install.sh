#!/bin/bash

var=$(ps -ef | grep 'gunicorn' | grep -v 'grep')
pid=$(echo ${var} | cut -d " " -f2)
if [ -n "${pid}" ]
then 
    sudo kill -9 ${pid}
    echo ${pid} is terminated.
else
    echo ${pid} is not running.
fi

rm -rf /home/ubuntu/recipe_BE
mkdir  /home/ubuntu/recipe_BE
