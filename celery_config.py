import os
from celery import Celery


# Initialization of the Celery object
celery_app = Celery(
    "shortener",  # Celery application name
    broker=os.environ.get("REDIS_VAR", "redis://redis:6379"),
    backend=os.environ.get("REDIS_VAR", "redis://redis:6379"),
    include=["worker.tasks"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Warsaw",
    broker_connection_retry_on_startup=True,
    enable_utc=True,
)

# Importing tasks into Celery
celery_app.autodiscover_tasks()

if __name__ == "__main__":
    celery_app.start()
