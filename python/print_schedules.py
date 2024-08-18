from crontab import CronTab

def main():
    cron = CronTab(tabfile='/etc/cron.d/retic', user=False)
    for job in cron:
        print(job)
        # print("dow %s" % (job.dow))
        # print("dow type %s" % (type(job.dow)))
        # for dow in job.dow:
            # print("dow item %s" % (dow))
            # print("dow item type %s" % (type(dow)))


if __name__ == "__main__":
    main()


