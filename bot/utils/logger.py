from datetime import datetime
import json
from ..models import BotMessage


class MessageLogger(object):
    """MessageLogger

    Class for logging messages our bot receives.
    """

    """Bot message utilities

    Use the following to get an existing or building a new BotMessage.
    """
    def get_bot_message(self, mid):
        try:
            return BotMessage.objects.get(mid=mid)
        except BotMessage.DoesNotExist:
            return None

    def get_bot_messages(self, timestamp, params=None):
        if not params:
            params = {}

        params['timestamp__lte'] = timestamp
        return BotMessage.objects.filter(**params)

    def build_bot_message(self, event):
        return BotMessage(
            sender_id=event.sender.id,
            recipient_id=event.recipient.id,
        )

    def log(self, event):
        """log

        Master log function.
        """
        if event.is_message:
            self.log_message(event)
        elif event.is_postback:
            self.log_postback(event)
        elif event.is_delivery:
            self.log_delivery(event)
        elif event.is_read:
            self.log_read(event)

    def log_message(self, event):
        bm = self.build_bot_message(event)
        payload = {'message': event.message}

        bm.mid = event.message['mid']
        bm.seq = event.message['seq']
        bm.received = event.is_received
        bm.timestamp = event.timestamp
        bm.payload = json.dumps(payload)

        bm.save()

    def log_postback(self, event):
        bm = self.build_bot_message(event)
        payload = {'postback': event.postback}

        bm.timestamp = event.timestamp
        bm.payload = json.dumps(payload)

        bm.save()

    def log_delivery(self, event):
        watermark = datetime.utcfromtimestamp(event.delivery['watermark']/1000)
        bms = self.get_bot_messages(watermark, {'delivered_time__isnull': True})
        for bm in bms:
            bm.delivered_time = watermark
            bm.save()

    def log_read(self, event):
        watermark = datetime.utcfromtimestamp(event.read['watermark']/1000)
        bms = self.get_bot_messages(watermark, {'read_time__isnull': True})
        for bm in bms:
            bm.read_time = watermark
            bm.save()
