from .models import user, messages
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ('userid', 'username', 'IdentityPub',
                  'SignedPub', 'OneTimePub')


class MessagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = messages
        fields = ('message_id', 'fromUserid', 'toUserid',
                  'date', 'ciphertext')
