from .models import user, friends
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ('userid', 'username', 'IdentityPub', 'SignedPub',
                  'OneTimePub', 'friends', 'last_ip', 'last_port')
