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

    def create_bot_message(self, event, payload):
        received = not event.is_echo
        bot_id = event.sender.id if received else event.recipient.id

        return BotMessage.objects.create(
            bot_id=bot_id,
            timestamp=event.timestamp,
            received=received,
            payload=json.dumps(payload),
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
        """log_message

        Logs a message event.
        """
        payload = {'message': event.message}
        self.create_bot_message(event, payload)

    def log_postback(self, event):
        """log_postback

        Logs a postback event.
        """
        payload = {'postback': event.postback}
        self.create_bot_message(event, payload)

    def log_delivery(self, event):
        """log_read

        Logs a delivery event by getting all messages upto watermark timestamp and
        setting their delivery times.
        """
        watermark = datetime.utcfromtimestamp(event.delivery['watermark']/1000)
        params = {
            'bot_id': event.sender.id,
            'received': False,
            'delivered_time__isnull': True,
        }

        bms = self.get_bot_messages(watermark, params)
        for bm in bms:
            bm.delivered_time = watermark
            bm.save()

    def log_read(self, event):
        """log_read

        Logs a read event by getting all messages upto watermark timestamp and
        setting their read times.
        """
        watermark = datetime.utcfromtimestamp(event.read['watermark']/1000)
        params = {
            'bot_id': event.sender.id,
            'received': False,
            'delivered_time__isnull': False,
            'read_time__isnull': True,
        }

        bms = self.get_bot_messages(watermark, params)
        for bm in bms:
            bm.read_time = watermark
            bm.save()
