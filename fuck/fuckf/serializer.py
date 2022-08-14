from django.contrib.auth.models import User, Group
from rest_framework import serializers
from fuckf.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class BoardSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    contents = serializers.CharField(style={'base_template': 'textarea.html'})
    # author = serializers.StringRelatedField(many=True)
    author = serializers.CharField()
    
    created_at = serializers.DateTimeField()
    recently_modified_at = serializers.DateTimeField()
    visited_at = serializers.DateTimeField()

    class Meta:
        model = Board
        fields = ("title", "contents", "author", "created_at", "recently_modified_at", "visited_at")
 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Board.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.contents = validated_data.get('contents', instance.contents)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.recently_modified_at = validated_data.get('recently_modified_at', instance.recently_modified_at)
        instance.visited_at = validated_data.get('visited_at', instance.recently_modified_at)
        instance.save()
        return instance

    
    