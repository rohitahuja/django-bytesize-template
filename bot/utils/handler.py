from messenger import (
    Message,
    Webhook,
)

from base.handler import BaseMessageHandler


def handle_payload(payload, should_log=False):
    handler = MessageHandler()

    wh = Webhook(payload)
    for entry in wh.entries:
        for event in entry.messaging:
            handler.handle(event=event, should_create_user=True, should_log=should_log)


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

    def handle_delivery(self, event):
        """handle_delivery

        Handles a delivered message, which are given when a message we sent is delivered.
        """
        raise NotImplementedError

    def handle_read(self, event):
        """handle_read

        Handles a read message, which are those read by the user.
        """
        raise NotImplementedError

    def handle_echo(self, event):
        """handle_echo

        Handles an echoed message, which are those that we send.
        """
        raise NotImplementedError

    def handle_received_quick_reply(self, event):
        """handle_received_quick_reply

        Handles a message that indicates a tapped quick reply.
        """
        # text = "Thanks for the quick reply message!\n\n%s" % event.message['text']
        # return Message(text=text)
        raise NotImplementedError

    def handle_received_text(self, event):
        """handle_received_text

        Handles a message that contains text.
        """
        # text = "Thanks for the following message!\n\n%s" % event.message['text']
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
        #     return Message(text=text)

        # return None

        raise NotImplementedError
