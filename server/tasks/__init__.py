from datetime import datetime, timedelta

from utils.args import Args
from utils.tasks import TasksHandler

from .clean import clean
from .job_worker import job_worker

TasksHandler(dry=False, log=not Args.dev, DEV=Args.dev)

# If DEV, run at current time + 10 min, else run at 24:00
start_time = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute + 10) if Args.dev else timedelta(hours=24)


if not Args.dev:
	TasksHandler.set(
		'clean',
		start_time=start_time,
		interval=timedelta(weeks=1)
	)(clean)

for i in range(max(min(Args.job_workers, 10), 1)):
	TasksHandler.set(
		f'job-worker-{i}',
		interval=timedelta(seconds=3)
	)(job_worker)