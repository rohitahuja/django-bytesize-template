from datetime import datetime
from messages import (
    Sender,
    Recipient,
)


class WebhookMessaging(object):
    """WebhookMessaging

    Wrapper class for a messaging object sent to the webhook.
    Ref: https://developers.facebook.com/docs/messenger-platform/webhook-reference

    Parameters
    ----------
    sender: integer
        id of sender

    recipient: integer
        id of recipient

    timestamp: integer
        timestamp of messaging object if available (epoch time in milliseconds)

    kwargs: dict
        additional fields of messaging object

    Attibutes
    ---------
    Note that attributes of this class are the top level keys
    of the messaging object sent to the webhook.

    For example, if the message event payload is:
        {
            "sender": {
                "id":"USER_ID"
            },
            "recipient": {
                "id":"PAGE_ID"
            },
            "timestamp": 1458692752478,
            "message": {
                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                "seq": 73,
                ...
            }
        }

    The attributes will be:
        sender
        recipient
        timestamp
        message
    with their values as provided in the messaging object payload.
    """
    def __init__(self, sender, recipient, timestamp=None, **kwargs):
        self.sender = Sender(id=sender['id'])
        self.recipient = Recipient(id=recipient['id'])
        if timestamp is not None:
            # TODO: Validate time
            self.timestamp = datetime.utcfromtimestamp(timestamp / 1000)

        for key, value in kwargs.items():
            self.__dict__[key] = value

    """is_{{ type }}

    The following methods return a bool on whether or not
    the messaging object is { type }.
    """

    @property
    def is_delivery(self):
        """is_delivery

        Delivered messaging objects notify us that a message we sent has been
        delivered.
        """
        return hasattr(self, 'delivery')

    @property
    def is_message(self):
        """is_message

        Message messaging objects are those that a user sends to the bot.
        """
        return hasattr(self, 'message')

    @property
    def is_postback(self):
        """is_postback

        Postback messaging objects are sent when a postback button is tapped.
        """
        return hasattr(self, 'postback')

    @property
    def is_read(self):
        """is_read

        Read messaging objects are sent when a user reads a message we sent.
        """
        return hasattr(self, 'read')

    """is_{{ type }}

    The following is_{{ type }} methods are specifically for
    messaging objects.
    """

    @property
    def is_received(self):
        """is_received

        Received messaging objects are those that our bot receives.
        """
        return self.is_message and not self.message.get('is_echo', False)

    @property
    def is_echo(self):
        """is_echo

        Echo messaging objects are echoes of the messages that we send.
        """
        return self.is_message and self.message.get('is_echo', False)

    @property
    def has_quick_reply(self):
        """has_quick_reply

        The messaging object contains a tapped quick reply.

        Note that if this is the case, the payload for that quick_reply is
        sent back. A quick reply message will also have text (the title of the
        quick reply).
        """
        return self.is_message and 'quick_reply' in self.message

    @property
    def has_text(self):
        """has_text

        The messaging object contains text.

        Note that having text and having attachments are mutually exclusive.
        """
        return self.is_message and 'text' in self.message

    @property
    def has_attachments(self):
        """has_attachments

        The messaging object contains attachments.

        Note that having text and having attachments are mutually exclusive.
        """
        return self.is_message and 'attachments' in self.message


class WebhookEntry(object):
    """WebhookEntry

    Wrapper classes for messages in webhook payload.

    Parameters
    ----------
    id: integer
        the page id

    time: integer
        time of update (epoch time in milliseconds)

    messaging: array
        objects related to messaging
    """
    def __init__(self, id, time, messaging):
        self.id = id
        # TODO: Validate time
        self.time = datetime.utcfromtimestamp(time / 1000)
        self.messaging = [
            WebhookMessaging(**m) for m in messaging
        ]


class Webhook(object):
    """Webhook

    Wrapper class for payload received by webhook.

    Parameters
    ----------
    payload: dict
        payload recevied by webhook

    """
    def __init__(self, payload):
        self.payload = payload

    @property
    def entries(self):
        return [
            WebhookEntry(**e) for e in self.payload['entry']
        ]
