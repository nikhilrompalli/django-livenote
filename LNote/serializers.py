from rest_framework import serializers
from LNote.models import *

from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from django.conf.global_settings import AUTH_USER_MODEL as Account

class NoteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = noteBook
        fields = ('id','title','tag','time','user')




class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = note
        fields = ('id', 'title', 'tag', 'text', 'time','status','notebook')

class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = sharedNote
        fields = ('id','title','text','time','sharedById', 'sharedByName', 'sharedWithId', 'note')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')