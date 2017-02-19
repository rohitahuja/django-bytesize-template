import json
import logging
import traceback
from messenger import (
    Message,
    Webhook
)

from base.handle import BaseMessageHandler

logger = logging.getLogger(__name__)


def handle_payload(data):
    """handle_payload

    Asynchronous task to handle message event payload.
    """
    payload = json.loads(data)
    wh = Webhook(payload)

    handler = MessageHandler()
    for entry in wh.entries:
        for event in entry.messaging:
            try:
                handler.handle(event)
            except:
                logger.error(traceback.format_exc())


class MessageHandler(BaseMessageHandler):
    """MessageHandler

    Application message handler. To handle message cases, should override the methods that have
        raise NotImplementedError

    Please take a look at the BaseMessageHandler class in base/handler.py to see the methods and attributes
    available for use. Additionally, it's possible that not all the handlers need overriding. Just get rid
    of it if it isn't necessary.

    They should also have the following signature:

    Parameters
    ----------
    event: WebhookMessaging object
        message event to handle

    Returns
    -------
    message: Message object
        message to send to the user or None if it cannot be handled

    or

    messages: List of Message objects
        messages to send to the user
    """

    def handle(self, event):
        """handle

        Master message handler method.

        Currently calls the parent's handle method (which is necessary), but use this to add
        handle defaults and customization such as:
         - creating a user for some or all cases (see get_bot_user() and create_bot_user())
         - logging specifc messages (setting the should_log for certain cases)

        Parameters
        ----------
        event: WebhookMessaging object
            message event to handle
        """
        # Attach bot user object to event for access later on
        # if event.is_received or event.is_postback:
        #     event.bot_user = self.get_bot_user(event.sender) or self.create_bot_user(event.sender)

        return super(MessageHandler, self).handle(event=event)

    def handle_received_text(self, event):
        """handle_received_text

        Handles a message that contains text. This can contain text, quick replies, etc.
        """
        # if 'quick_reply' in event.message:
        #     text = "Thanks for the quick reply message!\n\n%s" % event.message['text']
        # else:
        #     text = "Thanks for the following message!\n\n%s" % event.message['text']

        # return Message(text=text)

        raise NotImplementedError

    def handle_received_attachments(self, event):
        """handle_received_attachments

        Handles a message that contains attachments.
        """
        # attachments = event.message['attachments']
        # for attachment in attachments:
        #     if attachment['type'] == "image":
        #         pass
        #     elif attachment['type'] == 'audio':
        #         pass
        #     elif attachment['type'] == 'video':
        #         pass
        #     elif attachment['type'] == 'file':
        #         pass
        #     elif attachment['type'] == 'template':
        #         pass
        #     elif attachment['type'] == 'fallback':
        #         pass
        #     else:
        #         return

        # text = "Thanks for your attachment(s)!"
        # return Message(text=text)

        raise NotImplementedError

    def handle_postback(self, event):
        """handle_postback

        Handles a postback, which are those in which a user taps a button.
        """
        # payload = event.postback['payload']
        # if payload.startswith('get_started,'):
        #     text = "Welcome to our bot!"
        # else:
        #     text = "Couldn't handle postback. :("

        # return Message(text=text)

        raise NotImplementedError
