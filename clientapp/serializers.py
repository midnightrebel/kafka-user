import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Message, User, TeamLeader, Office


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Message(**validated_data)

    class Meta:
        model = Message
        fields = ['content']


class TeamLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamLeader
        fields = ['email', 'username']



class OfficeCreateSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=255)

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
            raise ValidationError("Офис уже существует")
        return data


class OfficeUpdateSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=255)

    def validate(self, data):
        place = data['location']
        if place != '':
            office_instance = Office.objects.filter(location=place)
        if not office_instance.exists():
            raise ValidationError("Офиса не существует в базе.")
        return data

    class Meta:
        model = Office
        fields = ['location']


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    office = OfficeUpdateSerializer(many=True)
    teamleader = serializers.SlugRelatedField(queryset=TeamLeader.objects.all(), read_only=False, slug_field='username')

    def validate(self, data):
        username = data['username']
        email = data['email']
        if re.match(r'\d', username):
            raise ValidationError("Имя пользователя не должно начинаться с цифры.")
        if re.match(r'\d', email):
            raise ValidationError("Почта пользователя не должно начинаться с цифры.")
        if username != '' and email != '':
            username_instance = User.objects.filter(username=username)
            email_instance = User.objects.filter(email=email)
        else:
            raise ValidationError("Пустое поле почты или имени пользователя")
        return data

    class Meta:
        model = User
        fields = ('password', 'email', 'username', 'teamleader', 'password', 'office', 'job_title')

    def get_or_update_offices(self, offices):
        offices_ids = []
        for office in offices:
            office_instance, created = Office.objects.update_or_create(location=office.get('location'))
            offices_ids.append(office_instance.pk)
        return offices_ids

    def create_or_update_offices(self, offices):
        offices_ids = []
        for office in offices:
            office_instance, created = Office.objects.update_or_create(location=office.get('location'))
            offices_ids.append(office_instance.pk)
        return offices_ids

    def create(self, validated_data):
        office = validated_data.pop('office', [])
        user = User.objects.create(**validated_data)
        user.office.set(self.get_or_update_offices(office))
        return user

    def update(self, instance, validated_data):
        office = validated_data.pop('office')
        instance.teamleader = validated_data.get('teamleader')
        instance.office.set(self.create_or_update_offices(office))
        fields = ('password', 'email', 'username', 'teamleader', 'password', 'office', 'job_title')
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
                instance.set_password(validated_data['password'])
            except KeyError:
                pass
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    teamleader = serializers.StringRelatedField()
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'teamleader', 'password', 'office', 'job_title']


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
