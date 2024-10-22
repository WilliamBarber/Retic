#!/usr/bin/python3
import json
import sys
import os
sys.path.append('/usr/lib/Retic_Controller/python')
from schedule import pushScheduleUpdate, JobSpec
from crontab import CronTab

schedule_number = int(os.environ.get('PATH_INFO')[1:])
schedule_info = json.load(sys.stdin)

days_of_week = schedule_info['days_of_week']
start_hour = int(schedule_info['start_hour'])
start_minute = int(schedule_info['start_minute'])
duration = int(schedule_info['duration'])
enabled = bool(schedule_info['enabled'])

pushScheduleUpdate(schedule_number, JobSpec(days_of_week, start_hour, start_minute, duration, enabled), CronTab(user='www-data'))
