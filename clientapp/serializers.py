import re


from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Message, User, TeamLeader, Office


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ['content']


class TeamLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ['email', 'username']


class TeamLeadCreate(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ['email', 'username']


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['location']


class OfficeCreate(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['location']

    def validate(self, data):
        place = data['location']
        if re.match(r'\d', data['location']):
            raise ValidationError("Название не должно начинаться с цифры.")
        if place != '':
            office_instance = Office.objects.filter(location=place)
        if office_instance.exists():
            raise ValidationError("Магазин уже существует")
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
