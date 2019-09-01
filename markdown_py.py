from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def my_job():
	times = datetime.datetime.now()
	print('Hello World')
	print(times)

sched = BlockingScheduler()
sched.add_job(my_job, 'interval', seconds=10)
sched.start()