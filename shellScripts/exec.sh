#!/bin/bash

cd /home/ec2-user/footopia

if [-d "instance/log"]
then
	mkdir -p instance/log 
fi

source env/bin/activate
python app.py &> instance/log/footopia-$(date +%y-%m-%d).log