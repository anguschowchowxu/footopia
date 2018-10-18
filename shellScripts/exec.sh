#!/bin/bash

HOMEDIR="/home/ec2-user/footopia"

if [-d "$HOMEDIR/instance/log"]
then
	mkdir -p ${HOMEDIR}/instance/log 
fi

source env/bin/activate
python app.py &> /home/instance/log/footopia-$(date +%y-%m-%d).log