from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from dex.models import Org, BasePerson, Events


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    host_org = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ('name', 'time', 'host_org')


class BasePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePerson
        fields = '__all__'
