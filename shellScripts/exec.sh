#!/bin/bash

BASEDIR="/home/ec2-user/footopia"

if [ ! -d "${HOMEDIR}/instance/log" ]
then
	mkdir -p ${BASEDIR}/instance/log 
fi

source ${BASEDIR}/env/bin/activate
python app.py &> ${BASEDIR}/instance/log/footopia-$(date +%y-%m-%d).log