from time import timezone
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from fuckf.models import *
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password

from  django.utils import timezone



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    # Post = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all()) #reverse relationship
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']#, 'Post']





class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    contents = serializers.CharField(style={'base_template': 'textarea.html'})
    author = serializers.ReadOnlyField(source="user.username")
    
    created_at = serializers.DateTimeField()
    recently_modified_at = serializers.DateTimeField()
    visited_at = serializers.DateTimeField()

    class Meta:
        model = Post
        fields = ("title", "contents", "author", "created_at", "recently_modified_at", "visited_at")
 

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

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

from .models import *
class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="user.username")
    # category = PostSerializer()

    class Meta:
        model = Post 
        fields = ("title", "contents", "author", "category")

    # def create(self, validated_data):
        
    #     print("val data :", self.validated_data)
        
    #     return Post.objects.create(**validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post 
        fields = ['title', 'contents', 'author']

    def update(self, instance, validated_data):
        pass

    def save(self, **kwargs):
        pass

    









class PostCategorySerializer(serializers.ModelSerializer):
    # parent_category = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    
    class Meta:
        model = PostCategory
        fields = ("parent_category","name", "is_private")
    


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.title)
        instance.parent_category = validated_data.get('parent_category', instance.contents)
        instance.recently_modified_at = serializers.DateTimeField()
        instance.save()
        return instance


class PostCategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    
    class Meta:
        model = PostCategory
        fields = ("name", "is_private")
    
    def __init__(self, *args, **kwargs):
        if kwargs['data'].get('parent_category'):
            self.Meta.fields = list(self.Meta.fields)
            self.Meta.fields.append('parent_category')
        super(PostCategoryCreateSerializer, self).__init__(*args, **kwargs)



    def create(self, validated_data=None):
        return PostCategory.objects.create(**self.validated_data)
