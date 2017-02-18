from .. import MessengerObject


class Greeting(MessengerObject):
    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {'text': self.text}


class Payload(MessengerObject):
    def __init__(self, payload):
        self.payload = payload

    def to_dict(self):
        return {'payload': self.payload}


class MenuItem(MessengerObject):

    MENU_ITEM_TYPES = (
        'web_url', 'postback'
    )

    def __init__(self, item_type, title, url=None, payload=None):
        """
        Menu item object for call_to_actions array.
        Currently does not include webview_height_ratio and messenger_extension.
        """
        if item_type not in self.MENU_ITEM_TYPES:
            raise ValueError('<MenuItem> menu item type invalid, must one of %s' % str(self.MENU_ITEM_TYPES))

        self.type = item_type
        self.title = title
        self.url = url
        self.payload = payload

    @staticmethod
    def create_postback(title, payload):
        item_type = 'postback'
        return MenuItem(item_type=item_type, title=title, payload=payload)

    @staticmethod
    def create_web_url(title, url):
        item_type = 'web_url'
        return MenuItem(item_type=item_type, title=title, url=url)

    def to_dict(self):
        data = {'type': self.type, 'title': self.title}
        if self.url:
            data['url'] = self.url
        if self.payload:
            data['payload'] = self.payload
        return data


class CallToActions(MessengerObject):

    PAYLOAD_LIMIT = 1
    MENU_ITEMS_LIMIT = 5

    def __init__(self):
        self.call_to_actions = []

    def add_action(self, action, limit):
        if len(self.call_to_actions) == limit:
            raise ValueError('<CallToActions> number of actions cannot exceed %s' % limit)
        self.call_to_actions.append(action)

    def add_payload(self, payload):
        self.add_action(payload, self.PAYLOAD_LIMIT)

    def add_menu_item(self, menu_item):
        self.add_action(menu_item, self.MENU_ITEMS_LIMIT)

    def to_dict(self):
        return [
            cta.to_dict() for cta in self.call_to_actions
        ]
