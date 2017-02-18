from .. import MessengerObject


class Button(MessengerObject):
    def __init__(self, title):
        if len(title) > 20:
            raise ValueError('Button title limit is 20 characters')
        self.title = title

    def to_dict(self):
        data = {
            'type': self.button_type,
            'title': self.title
        }
        if self.button_type == 'web_url':
            data['url'] = self.url
        elif self.button_type == 'postback':
            data['payload'] = self.payload
        return data


class PostbackButton(Button):
    button_type = 'postback'

    def __init__(self, title, payload):
        self.payload = payload
        super(PostbackButton, self).__init__(title=title)


class WebUrlButton(Button):
    button_type = 'web_url'

    def __init__(self, title, url):
        self.url = url
        super(WebUrlButton, self).__init__(title=title)
