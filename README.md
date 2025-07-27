# twamp
## Twamp protocol based monitoring script collection
### Install instructions:
 - mkdir /opt/twampy
 - cd /opt/twampy/
 -  git clone https://github.com/nokia/twampy

### Install neccessary python modules (Python3):
 - sudo apt install python3 python3-pip
 - pip3 install python-dotenv

### If Python is not installed:
 - apt-get update
 - apt-get install python3

### Run Python in virtual environment:
 - python3 -m venv /opt/twampy/python3
 - cd /opt/twampy/python3/
 - ./bin/pip3 install python-dotenv
 - ./bin/pip3 install pymysql
 - source /opt/twampy/python3/bin/activate
 - Need to modify run.sh:
   - From: python3 /opt/twampy/process.py
   - To: /opt/twampy/python3/bin/python3 /opt/twampy/process.py
  
### Add to cron: run script in every seconds
#### * * * * * /opt/twampy/run.sh

### Configure twamp script:
- twamp_responder=87.229.6.134          //the IP address of the destination server
- packet_count=900                 //how many packets will sending)
- timeout_in_ms=50                 //timeout in ms - set carefuly, have impact on sending time
- result_file=/opt/twampy/log.txt  //Do not change

### V1.0: 2025.05.27
 - run twamp every minutes
 - Store data in database
 - Graphs shows in Graphana
