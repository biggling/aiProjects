from celery import Celery
from tools.shared.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery("pod", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Auto-discover tasks
app.autodiscover_tasks(["tasks"])

# Import beat schedule
from schedule import CELERYBEAT_SCHEDULE
app.conf.beat_schedule = CELERYBEAT_SCHEDULE
