#!/usr/bin/python3
import json
import sys
import os
sys.path.append('/usr/lib/Retic_Controller/python')
from schedule import pushTemporarySchedule

schedule_info = json.load(sys.stdin)

start_hour = int(schedule_info['start_hour'])
start_minute = int(schedule_info['start_minute'])
duration = int(schedule_info['duration'])
stations_from_json = schedule_info['stations']
stations = []
for station in stations_from_json:
    stations.append(int(station))

pushTemporarySchedule(start_hour, start_minute, duration, stations)
