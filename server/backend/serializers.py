from .models import user
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ('userid', 'IdentityPub', 'SignedPub', 'OneTimePub',
                  'ElephantPub', 'IdentityPri', 'SignedPri', 'OneTimePri', 'ElephantPri', 'last_ip', 'last_port')
