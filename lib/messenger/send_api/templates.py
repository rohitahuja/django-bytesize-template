from .. import MessengerObject

class TemplateObject(MessengerObject):
    pass


class ButtonTemplate(TemplateObject):

    button_limit = 3
    template_type = "button"  # validate existence of template_type

    def __init__(self, text):
        self.text = text
        self.buttons = []

    def add_button(self, button):
        self.append(self.buttons, button, self.button_limit)

    def to_dict(self):
        return {
            'template_type': self.template_type,
            'text': self.text,
            'buttons': [
                button.to_dict() for button in self.buttons
            ]
        }


class GenericTemplate(TemplateObject):
    element_limit = 10
    template_type = "generic"

    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.append(self.elements, element, self.element_limit)

    def to_dict(self):
        return{
            'template_type': self.template_type,
            'elements': [
                element.to_dict() for element in self.elements
            ]
        }
