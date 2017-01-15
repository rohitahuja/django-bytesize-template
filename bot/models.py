from __future__ import unicode_literals

import os

from django.db import models

from messenger import (
    Sender,
    UserProfile,
)

token = os.environ.get('PAGE_ACCESS_TOKEN')


class BotUser(models.Model):
    """BotUser

    Model for storing users of our bot.
    """
    bot_id = models.CharField(max_length=30, primary_key=True)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def user_profile(self):
        if not hasattr(self, '_user_profile'):
            sender = Sender(id=self.bot_id)
            self._user_profile = UserProfile(token, sender)
        return self._user_profile

    @property
    def first_name(self):
        return self.user_profile.first_name

    @property
    def last_name(self):
        return self.user_profile.last_name

    @property
    def profile_pic(self):
        return self.user_profile.profile_pic

    @property
    def gender(self):
        return self.user_profile.gender

    def serialize(self):
        data = {'id': self.bot_id}

        if self.full_name.strip():
            data['name'] = self.full_name
        if self.profile_pic:
            data['profile_pic'] = self.profile_pic
        if self.gender:
            data['gender'] = self.gender

        return data


class BotMessage(models.Model):
    """BotMessage

    Model for storing messages our bot receives.
    """
    mid = models.CharField(max_length=30, blank=True)
    seq = models.PositiveIntegerField(null=True, blank=True)

    sender_id = models.CharField(max_length=30)
    recipient_id = models.CharField(max_length=30)
    timestamp = models.DateTimeField(db_index=True)
    received = models.BooleanField(default=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    read_time = models.DateTimeField(null=True, blank=True)

    # Generic payload column that will store messaging object as json string
    payload = models.TextField(blank=True)

    # Order by most recent message
    class Meta:
        ordering = ['-seq']

    @property
    def sent(self):
        return not self.received

    @property
    def read(self):
        return self.read_time is not None

    @property
    def delivered(self):
        return self.delivered_time is not None
