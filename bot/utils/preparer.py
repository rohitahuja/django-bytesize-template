import os
from common import enum

from messenger import (
    CallToActions,
    MenuItem,
    MessengerClient,
    Payload,
    ThreadSettingsRequest
)

token = os.environ.get('PAGE_ACCESS_TOKEN')


# Prepares thread settings in chat
class BotThreadPreparer(object):
    class PersistentMenuItem(enum.Enum):
        about = enum.Item(5, 'About')

    @property
    def menu_items(self):
        menu_items = [(item_id, title) for item_id, title in self.PersistentMenuItem]
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
