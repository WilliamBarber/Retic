from crontab import CronTab
import datetime
import subprocess

log_messages = True

class JobSpec:
    def __init__(self, days_of_week:list[str], start_hour:int, start_minute:int, duration:int, enabled:bool):
        logStatus(f"creating new JobSpec with hour {start_hour}, minute {start_minute}, duration {duration}, and status {enabled}")
        self.start_time = datetime.time(hour = start_hour, minute = start_minute)
        self.days_of_week = days_of_week
        self.duration = duration
        self.enabled = enabled

def dow_to_str(dow:int) -> str:
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    return days[dow]

def incrementDaysList(old_days:list[str]) -> list[str]:
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    new_days = []
    for old_day in old_days:
        new_index = (days.index(old_day) + 1) % len(days)
        new_days.append(days[new_index])
    return new_days


def updateJob(job, job_spec, i):
    old_date_time = datetime.datetime.combine(datetime.date(2024, 8, 1), job_spec.start_time)
    new_date_time = incrementTime(old_date_time, 0, i * job_spec.duration)
    days_of_week = job_spec.days_of_week
    if new_date_time.day > old_date_time.day:
        days_of_week = incrementDaysList(job_spec.days_of_week)
    new_time = new_date_time.time()
    job.dow.on(*days_of_week) 
    job.hour.on(new_time.hour)
    job.minute.on(new_time.minute)


def pushScheduleUpdate(schedule_number:int, job_spec:JobSpec, cron) -> None:
    logStatus(f"push update for schedule {schedule_number}")
    for i in range(6):
        current_job = next(cron.find_comment('schedule_%d_%d' % (schedule_number, i + 1)))
        updateJob(current_job, job_spec, i)

    current_job = next(cron.find_comment('schedule_%d_off' % schedule_number))
    updateJob(current_job, job_spec, 6)

    if job_spec.enabled:
        enableSchedule(schedule_number, cron)
    else:
        disableSchedule(schedule_number, cron)
    
    cron.write()
    logStatus("write cron changes")

def createTemporaryJob(start_time, increment, station):
    logStatus(f"create temporary job starting at {start_time} for station {station}")
    old_date_time = datetime.datetime.combine(datetime.date(2024, 8, 1), start_time)
    logStatus(f"old date_time created as {old_date_time}")
    new_date_time = incrementTime(old_date_time, 0, increment)
    logStatus(f"new date_time created as {new_date_time}")
    new_time = new_date_time.time()
    logStatus(f"new time created as {new_time}")
    time = ":".join(str(new_time).split(":")[:-1])
    if old_date_time.day != new_date_time.day:
        time += ' tomorrow'
    logStatus(f"job will be run at {time}")
    schedule_command = ['at', time]
    process = subprocess.Popen(schedule_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate('/usr/lib/Retic_Controller/retic %d' % station)
    if len(stdout) > 0:
        logStatus("at generated the following stdout: {str(stdout).rstrip()}")
    if len(stderr) > 0:
        logStatus(f"at generated the following stderr: {str(stderr).rstrip()}")
    logStatus("job added to queue")


def pushTemporarySchedule(start_hour:int, start_minute:int, duration:int, stations:list[int]):
    logStatus(f"push new temporary schedule starting at {start_hour}:{start_minute} and duration {duration}")
    start_time = datetime.time(hour = start_hour, minute = start_minute)
    for i in range(1, len(stations)):
        createTemporaryJob(start_time, duration * i, stations[i])
    createTemporaryJob(start_time, duration * len(stations), 0)
    subprocess.run(['/usr/lib/Retic_Controller/retic', '%d' % stations[0]])

def disableRetic(): 
    logStatus("disable retic (cancel temporary schedule)")
    atq_process = subprocess.run('atq', capture_output=True, text=True)
    cut_command = ['cut', '-f1']
    cut_process = subprocess.run(cut_command, input=atq_process.stdout, capture_output=True, text=True)
    for job_id in cut_process.stdout.split('\n')[:-1]:
        subprocess.run(['atrm', job_id])
        logStatus(f"removing job with id {job_id}")
    subprocess.run(["/usr/lib/Retic_Controller/retic", "0"])

def disableSchedule(schedule_number, cron) -> None:
    for job in cron:
        if job.comment.find('schedule_%d' % (schedule_number)) != -1:
            job.enable(False)
            logStatus(f"disable {job}")
    cron.write()
    logStatus("write cron changes") 

def enableSchedule(schedule_number, cron) -> None:
    for job in cron:
        if job.comment.find('schedule_%d' % (schedule_number)) != -1:
            job.enable()
            logStatus(f"enable {job}")
    cron.write()
    logStatus("write cron changes")

def getJobSpec(schedule_number, cron) -> JobSpec:
    logStatus(f"request getJobSpec for schedule number {schedule_number}")
    days = []
    for job in cron:
        if job.comment.find('schedule_%d' % (schedule_number)) != -1:
            logStatus("found job!")
            if len(days) < 1:
                for day in job.dow:
                    days.append(dow_to_str(day))
                hour = int(str(job.hour))
                minute = int(str(job.minute))
            else:
                duration = 0
                if hour == int(str(job.hour)):
                    duration = int(str(job.minute)) - minute
                else:
                    duration = (int(str(job.minute)) + 60) - minute
                return JobSpec(days, hour, minute, duration, job.is_enabled())
    logStatus(f"job not found")

def getActiveStation() -> int:
    completed_process = subprocess.run(["/usr/lib/Retic_Controller/status"], capture_output=True, text=True)
    return int(completed_process.stdout)

def incrementTime(start_date_time, hours, minutes):
    start_date_time += datetime.timedelta(hours = hours, minutes = minutes)
    return start_date_time

def logStatus(message):
    if log_messages:
        log_file = open("/usr/lib/Retic_Controller/messages.log", "a")
        print(message, file=log_file)
        log_file.close()


def main():
    # cron = CronTab(tabfile='/etc/cron.d/retic', user=False)
    # days = ['MON','WED', 'FRI','SUN'] 
    # job_spec = JobSpec(days, 5, 15, 10, True)
    # pushScheduleUpdate(1, job_spec, cron) 
    # print(getActiveStation())
    # pushTemporarySchedule(6, 30, 3, [1, 2, 3, 4, 5, 6])
    # disableRetic()
    print('hello')

if __name__ == "__main__":
    main()


