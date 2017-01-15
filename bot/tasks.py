import json
from celery import task

from messenger import Webhook

from .utils.handle import MessageHandler


@task(name="handle_payload")
def handle_payload(data):
    """handle_payload

    Asynchronous task to handle message payload.
    """
    payload = json.loads(data)
    wh = Webhook(payload)

    handler = MessageHandler()
    for entry in wh.entries:
        for event in entry.messaging:
            handler.handle(event)
