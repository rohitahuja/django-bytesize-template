from __future__ import unicode_literals

import os

from django.db import models

from messenger import (
    Sender,
    UserProfile,
)

token = os.environ.get('PAGE_ACCESS_TOKEN')


def user_field(f):
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return ''
    return decorated


class BotUser(models.Model):
    """BotUser

    Model for storing users of our bot.

    Note that the first_name, last_name, profile_pic, etc. of the user are retrieved lazily via
    the Messenger Platform API.
    """
    bot_id = models.CharField(max_length=30, primary_key=True)

    # used for user search only
    _first_name = models.CharField(max_length=35, blank=True)
    _last_name = models.CharField(max_length=35, blank=True)
    _gender = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        if not self.first_name and not self.last_name:
            return ""
        return ("%s %s" % (self.first_name, self.last_name)).strip()

    @property
    @user_field
    def first_name(self):
        return self.user_profile.first_name

    @property
    @user_field
    def last_name(self):
        return self.user_profile.last_name

    @property
    @user_field
    def profile_pic(self):
        return self.user_profile.profile_pic

    @property
    @user_field
    def gender(self):
        return self.user_profile.gender

    @property
    @user_field
    def locale(self):
        return self.user_profile.locale

    @property
    @user_field
    def timezone(self):
        return self.user_profile.timezone

    @property
    def sender(self):
        return Sender(id=self.bot_id)

    @property
    def user_profile(self):
        if not hasattr(self, '_user_profile'):
            try:
                self._user_profile = UserProfile(token, self.sender)
            except:
                self._user_profile = lambda: None
        return self._user_profile

    def set_user_fields(self):
        self._first_name = self.first_name
        self._last_name = self.last_name
        self._gender = self.gender

    def serialize(self):
        data = {'id': self.bot_id}

        if self.full_name.strip():
            data['name'] = self.full_name
        if self.profile_pic:
            data['profile_pic'] = self.profile_pic
        if self.gender:
            data['gender'] = self.gender
        if self.locale:
            data['locale'] = self.locale
        if self.timezone:
            data['timezone'] = self.timezone

        return data


class BotMessage(models.Model):
    """BotMessage

    Model for storing messages our bot receives.
    """
    bot_id = models.CharField(max_length=30, db_index=True)
    timestamp = models.DateTimeField(db_index=True)
    received = models.BooleanField(default=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    read_time = models.DateTimeField(null=True, blank=True)

    # Generic payload column that will store messaging object as json string
    payload = models.TextField(blank=True)

    # Order by most recent message
    class Meta:
        ordering = ['-timestamp']

    @property
    def sent(self):
        return not self.received

    @property
    def read(self):
        return self.read_time is not None

    @property
    def delivered(self):
        return self.delivered_time is not None
