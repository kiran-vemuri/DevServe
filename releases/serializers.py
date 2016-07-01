from django.contrib.auth.models import User, Group
from releases.models import Product, Component, Binary
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'name')


class BinarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Binary
        fields = ('id', 'name', 'url', 'notes', 'status')
