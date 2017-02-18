from .. import MessengerObject


class Element(MessengerObject):
    def __init__(self, title, image_url, subtitle):
        if len(title) > 80:
            raise ValueError('Element title limit is 80 characters!')

        if len(subtitle) > 80:
            raise ValueError('Element subtitle limit is 80 characters!')

        self.button_limit = 3

        self.title = title
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = []

    def add_button(self, button):
        self.append(self.buttons, button, self.button_limit)

    def to_dict(self):
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'image_url': self.image_url,
            'buttons': [
                button.to_dict() for button in self.buttons
            ]
        }
