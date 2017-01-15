import json
from celery import task
from celery.decorators import periodic_task
from celery.schedules import crontab

from messenger import Webhook

from .utils.handle import MessageHandler


@task(name="handle_payload")
def handle_payload(data):
    """handle_payload

    Asynchronous task to handle message event payload.
    """
    payload = json.loads(data)
    wh = Webhook(payload)

    handler = MessageHandler()
    for entry in wh.entries:
        for event in entry.messaging:
            handler.handle(event)


# Use the following as a model for creating periodically running tasks.
#
# See http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
#
# Feel free to remove or comment this out so this task doesn't get caught in the queue.
@periodic_task(name="cleanup_messages", run_every=(crontab(hour=7, minute=30, day_of_week=1)))
def cleanup_messages():
    """cleanup_messages

    Cleans up old messages based on given threshold.
    """
    # THRESHOLD = 5000

    # bm_count = BotMessage.objects.count()
    # if bm_count > THRESHOLD:
    #     num_delete = bm_count - THRESHOLD

    #     bms = BotMessage.objects.order_by('timestamp')
    #     bms[:num_delete].delete()
    pass
