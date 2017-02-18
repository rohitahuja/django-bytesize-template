import requests

from .. import (
    MessengerError,
    GRAPH_API_URL,
)


class UserProfile(object):
    # Additional fields: 'locale','timezone'
    available_fields = ('first_name',
                        'last_name',
                        'profile_pic',
                        'gender')

    def __init__(self, access_token, user):
        self.access_token = access_token
        self.user = user
        self.populate_user_info()

    def populate_user_info(self):
        fields = ','.join(self.available_fields)
        url = '{}/{}'.format(GRAPH_API_URL, self.user.id)
        params = {'access_token': self.access_token, 'fields': fields}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            MessengerError(
                **response.json()['error']
            ).raise_exception()
        self.data = response.json()
        for af in self.available_fields:
            if af in self.data:
                setattr(self, af, self.data[af])
