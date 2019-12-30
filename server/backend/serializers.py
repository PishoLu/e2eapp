from .models import user
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ('userid', 'username', 'IdentityPub', 'SignedPub', 'OneTimePub',
                  'last_ip', 'last_port')