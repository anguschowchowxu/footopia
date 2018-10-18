# footopia
a application of sharing daily life based on gis info, expresented on the 
map, using python flask microframe with leaflet. Running on a aws ec2 instance 
with mongodb-org-3.6

## Installation
```
$ pip install -r requirements.txt
```

## Usage
```bash
$ source env/bin/activate
$ python app.py 
```
or set as a system service
```bash
$ sudo cp shellScripts/footopia.service /etc/systemd/system
$ sudo systemctl enable footopia.service
$ sudo systemctl start footopia.service
```