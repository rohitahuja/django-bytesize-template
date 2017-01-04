from __future__ import unicode_literals

# Python imports
import os
from common import enum

# Django imports
from django.db import models

token = os.environ.get('PAGE_ACCESS_TOKEN')


class BotUser(models.Model):
    bot_id = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_pic = models.CharField(max_length=320, blank=True)
    gender = models.CharField(max_length=8, blank=True)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

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
    mid = models.CharField(max_length=30, primary_key=True)
    seq = models.PositiveIntegerField()

    sender_id = models.CharField(max_length=30)
    recipient_id = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    received = models.BooleanField(default=True)
    delivered = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    # Generic payload column that will store messaging object as json string
    payload = models.TextField(blank=True)

    class Meta:
        ordering = ['-seq']

    @property
    def sent(self):
        return not self.received
