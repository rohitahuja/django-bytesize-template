import os
from messenger import (
    MessengerClient,
    MessageRequest,
    SenderAction,
)

from ...models import BotUser
from ..log import MessageLogger

token = os.environ.get('PAGE_ACCESS_TOKEN')


class SenderActionHandler(object):
    """SenderActionHandler

    Class for sender action handling. Used to create a more realistic messaging experience
    with our bot.
    """

    def mark_seen(self, sender):
        action = SenderAction('mark_seen')
        return self.send_action(sender, action)

    def typing_on(self, sender):
        action = SenderAction('typing_on')
        return self.send_action(sender, action)

    def typing_off(self, sender):
        action = SenderAction('typing_off')
        return self.send_action(sender, action)

    def send_action(self, sender, action):
        request = MessageRequest(recipient=sender, sender_action=action)
        client = MessengerClient(token)
        return client.send(request)


class BaseMessageHandler(object):
    """BaseMessageHandler

    Base class for message handling. To handle each message case, inherit the class and
    override the handle methods with NotImplemented.
    """

    """Properties

    Lazily create attributes.
    """
    @property
    def action_handler(self):
        if not hasattr(self, '_action_handler'):
            self._action_handler = SenderActionHandler()
        return self._action_handler

    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            self._logger = MessageLogger()
        return self._logger

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
        bot_user = BotUser.objects.create(
            bot_id=sender.id)

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
            return self.client.send(request)

        # Check if message is a set of messages or a single message
        if type(message) is list:
            for m in message:
                send(m)
        else:
            send(message)

    """Message handling utilities

    The following are helpers for handling all types of receivable messages.
    """

    def handle(self, event, should_log=False):
        """handle

        Master message handler method.

        Parameters
        ----------
        event: WebhookMessaging object
            message event to handle

        should_log: bool
            indicates whether or not to log the message event
        """
        # Page received message
        if event.is_received or event.is_postback:
            # Mark it as seen and set typing to on
            self.action_handler.mark_seen(event.sender)
            self.action_handler.typing_on(event.sender)

        # Call appropriate message handler
        message = None
        if event.is_message:
            message = self.handle_message(event)
        elif event.is_postback:
            message = self.handle_postback(event)
        elif event.is_delivery:
            message = self.handle_delivery(event)
        elif event.is_read:
            message = self.handle_read(event)
        else:
            return

        # Set typing to off if necessary
        if event.is_received or event.is_postback:
            self.action_handler.typing_off(event.sender)

        # Send message
        if message:
            self.send_message(event.sender, message)

        # Log the event
        if should_log:
            self.logger.log(event)

    def handle_message(self, event):
        """handle_message

        Handles a message, which can be either an echo of our message or
        a received message by a user.
        """
        if event.is_echo:
            return self.handle_echo(event)
        else:
            return self.handle_received(event)

        return None

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

    def handle_delivery(self, event):
        """handle_delivery

        Handles a delivered message, which are given when a message we sent is delivered.

        It's likely that this doesn't need to be handled, so feel free to ignore overriding this method.
        """
        pass

    def handle_read(self, event):
        """handle_read

        Handles a read message, which are those read by the user.

        It's likely that this doesn't need to be handled, so feel free to ignore overriding this method.
        """
        pass

    def handle_echo(self, event):
        """handle_echo

        Handles an echoed message, which are those that we send.

        It's likely that this doesn't need to be handled, so feel free to ignore overriding this method.
        """
        pass

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
