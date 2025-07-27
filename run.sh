#!/bin/bash

logger "Start twampy"

export PATH=/usr/bin:/bin:/usr/local/bin

twamp_responder=87.229.6.134
packet_count=900
timeout_in_ms=50
result_file=/opt/twampy/log.txt

python3 /opt/twampy/twampy.py sender $twamp_responder -c $packet_count -i $timeout_in_ms > $result_file 2>&1

python3 /opt/twampy/process.py

logger "Stop twampv"

