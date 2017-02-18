from .. import MessengerRequest


class ThreadSettingsRequest(MessengerRequest):

    request_type = 'thread_settings'

    def __init__(self, setting_type, method, thread_state=None, call_to_actions=None, greeting=None):
        super(self.__class__, self).__init__(method)
        self.setting_type = setting_type
        self.thread_state = thread_state
        self.call_to_actions = call_to_actions
        self.greeting = greeting

    @staticmethod
    def create_call_to_actions_request(thread_state, method, call_to_actions=None):
        setting_type = 'call_to_actions'
        return ThreadSettingsRequest(
            setting_type=setting_type, method=method, thread_state=thread_state, call_to_actions=call_to_actions
        )

    @staticmethod
    def create_get_started_button(call_to_actions):
        return ThreadSettingsRequest.create_call_to_actions_request('new_thread', 'post', call_to_actions)

    @staticmethod
    def delete_get_started_button():
        return ThreadSettingsRequest.create_call_to_actions_request('new_thread', 'delete')

    @staticmethod
    def create_persistent_menu(call_to_actions):
        return ThreadSettingsRequest.create_call_to_actions_request('existing_thread', 'post', call_to_actions)

    @staticmethod
    def delete_persistent_menu():
        return ThreadSettingsRequest.create_call_to_actions_request('existing_thread', 'delete')

    @staticmethod
    def create_greeting(greeting):
        return ThreadSettingsRequest(setting_type='greeting', method='post', greeting=greeting)

    @staticmethod
    def delete_greeting():
        return ThreadSettingsRequest(setting_type='greeting', method='delete')

    def to_dict(self):
        data = {'setting_type': self.setting_type}
        if self.thread_state:
            data['thread_state'] = self.thread_state
        if self.call_to_actions:
            data['call_to_actions'] = self.call_to_actions.to_dict()
        if self.greeting:
            data['greeting'] = self.greeting.to_dict()
        return data

from entities import *
