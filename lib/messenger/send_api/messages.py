from .. import MessengerObject


class Message(MessengerObject):
    def __init__(self, text=None, attachment=None, quick_replies=None, metadata=None):
        if bool(text) == bool(attachment):
            raise ValueError('<Message> text or attachment must be set, but not both')

        self.text = text
        self.attachment = attachment
        self.quick_replies = quick_replies
        self.metadata = metadata

    def to_dict(self):
        data = {}
        if self.text:
            data['text'] = self.text
            if self.quick_replies:
                data['quick_replies'] = self.quick_replies.to_dict()
        if self.attachment:
            data['attachment'] = self.attachment.to_dict()
        if self.metadata:
            data['metadata'] = self.metadata
        return data


class Participant(MessengerObject):
    def __init__(self, id=None, phone_number=None):
        if not id and not phone_number:
            raise ValueError('<%s> id or phone_number must be set' % self.__class__.__name__)
        self.id = id
        self.phone_number = phone_number

    def to_dict(self):
        if self.id:
            return {'id': self.id}
        return {'phone_number': self.phone_number}


class Sender(Participant):
    pass


class Recipient(Participant):
    pass
