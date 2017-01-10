import os
from messenger import (
    MessengerClient,
    MessageRequest,
    SenderAction,
    UserProfile,
)

from ..models import BotUser
from logger import MessageLogger

token = os.environ.get('PAGE_ACCESS_TOKEN')


class SenderActionHandler(object):
    """SenderActionHandler

    Class for sender action handling. Used to create a more realistic messaging experience
    with our bot.
    """
    def __init__(self, event):
        self.event = event

    def mark_seen(self):
        action = SenderAction('mark_seen')
        return self.send_action(action)

    def typing_on(self):
        action = SenderAction('typing_on')
        return self.send_action(action)

    def typing_off(self):
        action = SenderAction('typing_off')
        return self.send_action(action)

    def send_action(self, action):
        request = MessageRequest(recipient=self.event.sender, sender_action=action)
        client = MessengerClient(token)
        return client.send(request)


class BaseMessageHandler(object):
    """BaseMessageHandler

    Base class for message handling. To handle each message case, inherit the class and
    override the handle methods with NotImplemented.

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
        self.action_handler = SenderActionHandler(event)
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

    def send_message(self, message):
        """send_message

        Sends message to event sender.
        """
        request = MessageRequest(recipient=self.event.sender, message=message)
        client = MessengerClient(token)
        return client.send(request)

    """Message handling utilities

    The following are helpers for handling all types of receivable messages.
    """

    def handle(self):
        """handle

        Master message handler method.
        """
        event = self.event

        # If we received message, mark it as seen and set typing to on
        if event.is_received or event.is_postback:
            self.action_handler.mark_seen()
            self.action_handler.typing_on()

        # Call appropriate message handler
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

        # Set typing to off if necessary
        if event.is_received or event.is_postback:
            self.action_handler.typing_off()

        if self.message is None:
            return

        # Check if message is a set of messages or a single message
        if type(self.message) is list:
            for message in self.message:
                self.send_message(message)
        else:
            self.send_message(self.message)

        # Log the event
        if self.logger:
            self.logger.log()

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
        if event.has_quick_reply:
            return self.handle_received_quick_reply(event)
        elif event.has_text:
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
        """
        pass

    def handle_read(self, event):
        """handle_read

        Handles a read message, which are those read by the user.
        """
        pass

    def handle_echo(self, event):
        """handle_echo

        Handles an echoed message, which are those that we send.
        """
        pass

    def handle_received_quick_reply(self, event):
        """handle_received_quick_reply

        Handles a message that indicates a tapped quick reply.
        """
        pass

    def handle_received_text(self, event):
        """handle_received_text

        Handles a message that contains text.
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
