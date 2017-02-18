from .. import MessengerRequest


class MessageRequest(MessengerRequest):

    NOTIFICATION_TYPE_OPTIONS = (
        'REGULAR', 'SILENT_PUSH', 'NO_PUSH'
    )

    request_type = 'messages'

    def __init__(self, recipient, message=None, sender_action=None, notification_type=None, method='post'):
        super(self.__class__, self).__init__(method)
        self.recipient = recipient
        self.message = message
        self.sender_action = sender_action
        if notification_type:
            if notification_type not in self.NOTIFICATION_TYPE_OPTIONS:
                raise ValueError(
                    'notification_type valid options %s' %
                    str(self.NOTIFICATION_TYPE_OPTIONS)
                )
        self.notification_type = notification_type

    def to_dict(self):
        data = {'recipient': self.recipient.to_dict()}
        if self.message:
            data['message'] = self.message.to_dict()
        if self.sender_action:
            data['sender_action'] = self.sender_action.to_dict()
        if self.notification_type:
            data['notification_type'] = self.notification_type
        return data

from attachments import *
from buttons import *
from messages import *
from quick_replies import *
from templates import *
from webhooks import *
from sender_actions import *
from elements import *
