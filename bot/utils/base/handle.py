import logging
import os
import traceback
from messenger import (
    MessengerClient,
    MessageRequest,
)

from ...models import BotUser

token = os.environ.get('PAGE_ACCESS_TOKEN')
logger = logging.getLogger(__name__)


class BaseMessageHandler(object):
    """BaseMessageHandler

    Base class for message handling. To handle each message case, inherit the class and
    override the handle methods with NotImplemented.
    """

    """Properties

    Lazily create attributes.
    """

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = MessengerClient(token)
        return self._client

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

    def create_bot_user(self, sender):
        """create_bot_user

        Creates a bot user

        Parameters
        ----------
        sender: Sender object
            the sender of the event, contained in self.event.sender

        Returns
        -------
        bot_user: BotUser object
            the created bot user
        """
        bot_user = BotUser(bot_id=sender.id)
        bot_user.set_user_fields()
        bot_user.save()

        return bot_user

    def send_message(self, sender, message):
        """send_message

        Sends message to event sender.

        Parameters
        ----------
        sender: Sender object
            the sender of the event, contained in self.event.sender

        message: Message object or list of Message objects
            the message to send to the sender
        """
        def send(m):
            request = MessageRequest(recipient=sender, message=m)
            try:
                return self.client.send(request)
            except:
                logger.error(traceback.format_exc())

        # Check if message is a set of messages or a single message
        if type(message) is list:
            for m in message:
                send(m)
        else:
            send(message)

    """Message handling utilities

    The following are helpers for handling all types of receivable messages.
    """

    def handle(self, event):
        """handle

        Master message handler method.

        Parameters
        ----------
        event: WebhookMessaging object
            message event to handle

        should_log: bool
            indicates whether or not to log the message event
        """

        # Call appropriate message handler
        message = None
        if event.is_received:
            message = self.handle_received(event)
        elif event.is_postback:
            message = self.handle_postback(event)
        else:
            return

        # Send message
        if message:
            self.send_message(event.sender, message)

    def handle_received(self, event):
        """handle_received

        Handles a received message, which are those that the user sends.
        """
        if event.has_text:
            return self.handle_received_text(event)
        elif event.has_attachments:
            return self.handle_received_attachments(event)

        return None

    """Note that the following methods are those that should be overriden.

    They should have the following:

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

    def handle_received_text(self, event):
        """handle_received_text

        Handles a message that contains text. This can contain text, quick replies, etc.
        """
        pass

    def handle_received_attachments(self, event):
        """handle_received_attachments

        Handles a message that contains attachments.
        """
        pass

    def handle_postback(self, event):
        """handle_postback

        Handles a postback, which are those in which a user taps a button.
        """
        pass
