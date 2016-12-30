import os
from common import enum

from models import (
    BotUser,
    BotMessage,
    PersistentMenuItem,
)

from messenger import (
    CallToActions,
    MenuItem,
    Message,
    MessengerClient,
    MessageRequest,
    Payload,
    ThreadSettingsRequest,
    UserProfile,
    Webhook,
)

token = os.environ.get('PAGE_ACCESS_TOKEN')


# Master payload handler function
def handle_payload(payload, log=False):
    wh = Webhook(payload)
    for entry in wh.entries:
        for event in entry.messaging:
            handler = BotMessageHandler(event)
            handler.handle(log)


# Master message handler class for received messages
#TODO MAKE MORE GENERAL AND ADAPTABLE TO CHANGE
class BotMessageHandler(object):
    def __init__(self, event):
        self.event = event
        self.bot_user = self.get_bot_user(event.sender) or self.create_bot_user(event.sender)
        self.message = None

    ## Bot user utils ##

    # Gets the corresponding bot user if it exists
    def get_bot_user(self, sender):
        try:
            return BotUser.objects.get(bot_id=sender.id)
        except BotUser.DoesNotExist:
            return None

    # Creates a bot user
    def create_bot_user(self, sender):
        try:
            user_profile = UserProfile(token, sender)
            data = user_profile.data
        except:
            data = {}

        bot_user = BotUser.objects.create(
            bot_id=sender.id,
            **data)

        return bot_user

    ## Message handler utils ##

    # Master message handler function
    def handle(self, log):
        event = self.event

        # retrieve appropriate message based on event type
        if event.is_received:
            # a message has been sent to our page
            self.message = self.handle_received(event)
        elif event.is_postback:
            # a Postback button, Get Started button, Persistent menu or Structured Message has been tapped
            self.message = self.handle_postback(event)
        else:
            # event is not recognized
            return

        if self.message is None:
            text = "Sorry! We couldn't understand your message. :("
            self.message = Message(text=text)

        self.send_message()

        if log:
            self.log()

    # Received message handler
    def handle_received(self, event):
        if event.has_text:
            return self.handle_received_text(event)
        elif event.has_attachments:
            return self.handle_received_attachment(event)

        return None

    # Received text handler
    def handle_received_text(self, event):
        # TODO
        return Message(text="Thanks for the following message!\n%s" % event.message['text'])

    # Received attachment handler
    def handle_received_attachment(self, event):
        attachments = event.message['attachments']
        text = "Thanks for your attachment(s)!"
        for attachment in attachments:
            if attachment['type'] == "image":
                # TODO
                pass
            elif attachment['type'] == 'video':
                # TODO
                pass

        # currently doesn't notify user of unhandled media
        return Message(text=text)

    # Cases in this function should reflect persistent menu items generated in bot/models.py
    def handle_postback(event):
        # TODO
        payload = event.postback['payload']
        if payload.startswith('get_started,'):
            return Message(text="Welcome to our bot!")
        return None

    ## Logging utils ##
    def log(self):
        self.log_event()
        self.log_message()

    def log_event(self):
        pass

    def log_message(self):
        pass

    # Message sender
    def send_message(self):
        request = MessageRequest(self.event.sender, self.message)
        client = MessengerClient(token)
        client.send(request)


# Prepares thread settings in chat
class BotThreadPreparer(object):
    class PersistentMenuItem(enum.Enum):
        about = enum.Item(5, 'About')

    @property
    def menu_items(self):
        menu_items = [(item_id, title) for item_id, title in PersistentMenuItem]
        menu_items.sort()
        return menu_items

    # Master prepare function
    def prepare(self):
        self.prepare_get_started()
        self.prepare_persistent_menu()

    # Prepares persistent menu in chat with PersistentMenuItem enumerator
    def prepare_persistent_menu(self):
        call_to_actions = CallToActions()
        for item_id, title in self.menu_items:
            menu_item = MenuItem.create_postback(title=title, payload='menu_item,%s' % item_id)
            call_to_actions.add_menu_item(menu_item)

        self.send_thread_settings(call_to_actions)

    # Prepares get started screen
    def prepare_get_started(self):
        call_to_actions = CallToActions()
        payload = Payload('get_started,')
        call_to_actions.add_payload(payload)

        self.send_thread_settings(call_to_actions)

    # Applies thread settings to chat
    def send_thread_settings(self, call_to_actions):
        client = MessengerClient(token)
        request = ThreadSettingsRequest.create_persistent_menu(call_to_actions)
        client.send(request)
