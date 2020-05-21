#!/bin/bash

# OWN basic_app directory
command sudo chown -R $USER:$USER /var/www/basic_app
command python3 --version

# CREATE PYTHON3 ENVIROMENT
isEnv=`ls /var/www/basic_app/  | grep 'venv'`
if [[ ! $isEnv ]];then
  cd /var/www/basic_app
  command python3 -m venv venv
  command ls
fi

# ACTIVATE ENVIROMENT AND INSTALL REQUIREMENTS
command source /var/www/basic_app/venv/bin/activate
command pip3 install -r /var/www/basic_app/requirements.txt
command pip3 list
cd /var/www/basic_app
command python3 mbta_departures/manage.py makemigrations
command python3 mbta_departures/manage.py migrate
