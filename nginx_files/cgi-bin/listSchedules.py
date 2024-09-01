#!/usr/bin/python3
import sys
import json
from crontab import CronTab
sys.path.append('/usr/lib/Retic_Controller/python')
from schedule import getJobSpec

def convert_to_dict(schedule_number, job):
    return {
            'schedule_number': schedule_number,
            'job_spec': {
                'days_of_week': job.days_of_week,
                'start_hour': job.start_time.hour,
                'start_minute': job.start_time.minute,
                'duration': job.duration,
                'enabled': job.enabled,
            }
           }


print('Content-Type: text/json')
print('')
cron = CronTab(user='www-data')
jobs = [convert_to_dict(i, getJobSpec(i, cron)) for i in range(1, 4)]
print(json.dumps({'jobs': jobs}))
