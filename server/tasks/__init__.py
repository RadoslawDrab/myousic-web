from datetime import datetime, timedelta

from utils import get_env
from utils.tasks import TasksHandler

from .clean import clean

DEV = get_env('DEV', default=False, type=bool)
TasksHandler(dry=False, log=not DEV, DEV=DEV)

# If DEV, run at current time + 10 min, else run at 12:00
start_time = timedelta(hours=datetime.now().hour, minutes=datetime.now().minute + 10) if DEV else timedelta(hours=12)


TasksHandler.set(
	'clean',
	start_time=start_time,
	interval=timedelta(minutes=10) if DEV else timedelta(hours=12)
)(clean)