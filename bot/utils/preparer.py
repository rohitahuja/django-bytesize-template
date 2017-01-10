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


class BotThreadPreparer(object):
    """BotThreadPreparer

    Class for preparing thread settings in chat.
    """

    """Persistent menu utilities

    The following is for setting up the persistent menu options.
    This can and should later be changed to store menu items in DB.
    """
    class PersistentMenuItem(enum.Enum):
        about = enum.Item(5, 'About')

    @property
    def menu_items(self):
        """menu_items

        Returns items in PersistentMenuItem in sorted order by id.
        """
        menu_items = [(item_id, title) for item_id, title in self.PersistentMenuItem]
        menu_items.sort()
        return menu_items

    def prepare(self):
        """prepare

        Master prepare function.
        """
        self.prepare_get_started()
        self.prepare_persistent_menu()

    def prepare_persistent_menu(self):
        """prepare_persistent_menu

        Prepares persistent menu in chat with PersistentMenuItem enumerator.

        The payload that is received will be in the format:
            item_name,item_id
        """
        call_to_actions = CallToActions()
        for item_id, title in self.menu_items:
            menu_item = MenuItem.create_postback(title=title, payload='menu_item,%s' % item_id)
            call_to_actions.add_menu_item(menu_item)

        self.send_thread_settings(call_to_actions)

    def prepare_get_started(self):
        """prepare_get_started

        Prepares get started screen postback.
        """
        call_to_actions = CallToActions()
        payload = Payload('get_started,')
        call_to_actions.add_payload(payload)

        self.send_thread_settings(call_to_actions)

    def send_thread_settings(self, call_to_actions):
        """send_thread_settings

        Applies thread settings to chat
        """
        client = MessengerClient(token)
        request = ThreadSettingsRequest.create_persistent_menu(call_to_actions)
        return client.send(request)
