from .models import user, friends, messages
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ('userid', 'username', 'IdentityPub', 'SignedPub',
                  'OneTimePub', 'friends', 'last_ip', 'last_port')


class MessagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = messages
        fields = ('fromUserid', 'toUserid', 'date', 'plaintext')


class MessagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = friends
        fields = ('urerid', 'IP', 'Port', 'remark', 'status', 'group')
