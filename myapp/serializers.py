from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')  # Fields exposed via API
        extra_kwargs = {'password': {'write_only': True}}  # Password write-only for security

    def create(self, validated_data):
        # Use create_user to hash password properly
        return User.objects.create_user(**validated_data)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')  # Assuming room has 'name' field
        extra_kwargs = {'name': {'validators': []}}  # We override default validators to add custom uniqueness validation

    def validate_name(self, value):
        # Ensure room name is unique
        if Room.objects.filter(name=value).exists():
            raise serializers.ValidationError("Room with this name already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    room = RoomSerializer()  # Nested serializer for room info

    class Meta:
        model = Message
        # Include fields matching model definition
        fields = ('user', 'message', 'time_date', 'room')
        extra_kwargs = {'message': {'read_only': False}}  # Allow writing message content

    def create(self, validated_data):
        room_data = validated_data.pop('room')
        room, created = Room.objects.get_or_create(name=room_data['name'])
        message = Message.objects.create(room=room, **validated_data)
        return message
