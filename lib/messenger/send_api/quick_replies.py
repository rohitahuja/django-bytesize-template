from .. import MessengerObject


class QuickReply(MessengerObject):

    CONTENT_TYPE_OPTIONS = (
        'text', 'location'
    )

    def __init__(self, content_type, title=None, payload=None, image_url=None):
        if content_type not in self.CONTENT_TYPE_OPTIONS:
            raise ValueError('<QuickReply> content_type must be in %s', str(self.CONTENT_TYPE_OPTIONS))

        self.content_type = content_type
        if content_type == 'text':
            if not title and not payload:
                raise ValueError('<QuickReply> title and payload must be set')
            self.title = title
            self.payload = payload

        self.image_url = image_url

    def to_dict(self):
        data = {'content_type': self.content_type}
        if self.title:
            data['title'] = self.title
        if self.payload:
            data['payload'] = self.payload
        if self.image_url:
            data['image_url'] = self.image_url
        return data


class QuickReplies(MessengerObject):

    QUICK_REPLIES_LIMIT = 11

    def __init__(self):
        self.quick_replies = []

    def add_quick_reply(self, quick_reply):
        self.append(self.quick_replies, quick_reply, self.QUICK_REPLIES_LIMIT)

    def to_dict(self):
        return [
            qr.to_dict() for qr in self.quick_replies
        ]
