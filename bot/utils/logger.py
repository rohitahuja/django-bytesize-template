import json
from ..models import BotMessage


class MessageLogger(object):
    def __init__(self, event):
        self.event = event

    def get_bot_message(self, mid):
        try:
            return BotMessage.objects.get(mid=mid)
        except BotMessage.DoesNotExist:
            return None

    def build_bot_message(self, event):
        return BotMessage(
            mid=event.mid,
            seq=event.seq,
            sender_id=event.sender.id,
            recipient_id=event.recipient.id,
            timestamp=event.timestamp
        )

    def log(self):
        event = self.event
        bm = self.get_bot_message(event.mid) or self.build_bot_message(event)

        if event.is_message:
            self.log_message(event, bm)
        elif event.is_postback:
            self.log_postback(event, bm)
        elif event.is_delivery:
            self.log_delivery(event, bm)
        elif event.is_read:
            self.log_read(event, bm)
        else:
            return

        bm.save()

    def log_message(self, event, bm):
        bm.received = event.is_received

        payload = {'message': event.message}
        bm.payload = json.dumps(payload)

    def log_postback(self, event, bm):
        payload = {'postback': event.postback}
        bm.payload = json.dumps(payload)

    def log_delivery(self, event, bm):
        bm.delivered = True

    def log_read(self, event, bm):
        bm.read = True
