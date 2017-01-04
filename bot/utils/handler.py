import os

from ..models import BotUser

from messenger import (
    Message,
    MessengerClient,
    MessageRequest,
    UserProfile,
    Webhook,
)

from logger import MessageLogger

token = os.environ.get('PAGE_ACCESS_TOKEN')


def handle_payload(payload, log=False):
    wh = Webhook(payload)
    for entry in wh.entries:
        for event in entry.messaging:
            handler = MessageHandler(event=event, should_create_user=True, should_log=True)
            handler.handle()


class MessageHandler(object):
    """MessageHandler

    Class for message handling. To capture each message case, implement the
    handle methods with NotImplemented.

    Parameters
    ----------
    event: WebhookMessaging object
        message event to handle

    should_create_user: bool
        indicates whether or not to create a bot user if it does not exist

    should_log: bool
        indicates whether or not to log the message event
    """
    def __init__(self, event, should_create_user=False, should_log=False):
        self.event = event
        self.bot_user = (self.get_bot_user(event.sender) or
                        (should_create_user and self.create_bot_user(event.sender)))
        self.logger = MessageLogger(event) if should_log else None
        self.message = None

    """Bot user utilities

    The following are helpers for getting and creating a bot user.
    """

    def get_bot_user(self, sender):
        """get_bot_user

        Gets corresponding bot user if it exists

        Parameters
        ----------
        sender: Sender object
            the sender of the event, contained in self.event.sender

        Returns
        -------
        bot_user: BotUser object
            the corresponding bot user or None
        """
        try:
            return BotUser.objects.get(bot_id=sender.id)
        except BotUser.DoesNotExist:
            return None

    # Creates a bot user
    def create_bot_user(self, sender):
        """create_bot_user

        Creates a bot user with all its available user info if retrievable

        Parameters
        ----------
        sender: Sender object
            the sender of the event, contained in self.event.sender

        Returns
        -------
        bot_user: BotUser object
            the created bot user
        """

        # Fetch user info
        try:
            user_profile = UserProfile(token, sender)
            data = user_profile.data
        except:
            data = {}

        # Create bot user
        bot_user = BotUser.objects.create(
            bot_id=sender.id,
            **data)

        return bot_user

    """Message handling utilities

    The following are helpers for handling all types of receivable messages.
    """

    def handle(self):
        """handle

        Master message handler method.
        """
        event = self.event

        if event.is_message:
            self.message = self.handle_message(event)
        elif event.is_postback:
            self.message = self.handle_postback(event)
        elif event.is_delivery:
            self.message = self.handle_delivery(event)
        elif event.is_read:
            self.message = self.handle_read(event)
        else:
            return

        if self.message is None:
            return

        self.send_message()

        if self.logger:
            self.logger.log()

    """Note that the following handle_{{ type }} methods should have the following:

    Parameters
    ----------
    event: WebhookMessaging object
        message event to handle

    Returns
    -------
    message: Message object
        message to send to the user or None if it cannot be handled
    """

    def handle_delivery(self, event):
        pass

    def handle_read(self, event):
        pass

    def handle_message(self, event):
        """handle_message

        Handles a message, which can be either an echo of our message or
        a received message by a user.
        """
        if event.is_echo(event):
            return self.handle_echo(event)
        else:
            return self.handle_received(event)

        return None

    def handle_echo(self, event):
        """handle_echo

        Handles an echoed message, which are those that we send.
        """
        pass

    def handle_received(self, event):
        """handle_received

        Handles a received message, which are those that the user sends.
        """
        if event.has_quick_reply:
            return self.handle_received_quick_reply(event)
        elif event.has_text:
            return self.handle_received_text(event)
        elif event.has_attachments:
            return self.handle_received_attachments(event)

        return None

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

    def send_message(self):
        """send_message

        Sends message to event sender.
        """
        request = MessageRequest(self.event.sender, self.message)
        client = MessengerClient(token)
        return client.send(request)
