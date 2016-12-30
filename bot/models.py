from __future__ import unicode_literals

# Python imports
import os

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
    #all necessary attributes in messages
