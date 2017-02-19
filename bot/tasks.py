import json
from celery import task
from celery.decorators import periodic_task
from celery.schedules import crontab

from messenger import Webhook
from .utils.log import MessageLogger


@task(name="log_payload")
def log_payload(data):
    """log_payload

    Asynchronous task to log the message event payload.
    """
    payload = json.loads(data)
    wh = Webhook(payload)

    mlogger = MessageLogger()
    for entry in wh.entries:
        for event in entry.messaging:
            mlogger.log(event)


# Use the following as a model for creating periodically running tasks.
#
# See http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
# Be sure to make the scheduled time in UTC.
#
# Feel free to remove or comment this out so this task doesn't get caught in the queue.
@periodic_task(name="cleanup_messages", run_every=(crontab(hour=7, minute=30, day_of_week=1)))
def cleanup_messages():
    """cleanup_messages

    Cleans up old messages based on given threshold. This runs at 7:30am (UTC) every Monday.
    """
    # THRESHOLD = 5000

    # bm_count = BotMessage.objects.count()
    # if bm_count > THRESHOLD:
    #     num_delete = bm_count - THRESHOLD

    #     bms = BotMessage.objects.order_by('timestamp')
    #     bms[:num_delete].delete()
    pass
