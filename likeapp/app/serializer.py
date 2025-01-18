from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Like, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'gender', 'bio', 'photo', 'likes']

class LikeSerializer(serializers.ModelSerializer):
    user_from = user_to = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user_from', 'user_to']