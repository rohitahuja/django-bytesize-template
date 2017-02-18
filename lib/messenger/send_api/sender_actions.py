from .. import MessengerObject


class SenderAction(MessengerObject):
    SENDER_ACTIONS = (
        'mark_seen', 'typing_on', 'typing_off'
    )

    def __init__(self, sender_action):
        if sender_action not in self.SENDER_ACTIONS:
            raise ValueError(
                'sender_action valid options %s' %
                str(self.SENDER_ACTIONS)
            )
        self.sender_action = sender_action

    def to_dict(self):
        return self.sender_action
