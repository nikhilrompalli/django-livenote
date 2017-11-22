# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class noteBook(models.Model):
    title=models.CharField(max_length=128)
    tag=models.CharField(max_length=1000)
    time=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=True)

    def __unicode__(self):
        return self.title

class note(models.Model):
    title=models.CharField(max_length=128)
    tag=models.CharField(max_length=1000)
    text=models.TextField(null=True)
    time=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    notebook = models.ForeignKey(noteBook, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title

class sharedNote(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add=True)
    sharedById = models.IntegerField()
    sharedByName = models.CharField(max_length=128)
    sharedWithId=models.IntegerField()
    note = models.ForeignKey(note)

    def __unicode__(self):
        return self.sharedByName