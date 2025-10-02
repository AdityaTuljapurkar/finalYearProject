from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link message to user
    message = models.TextField()  # Message content
    time_date = models.DateTimeField(default=timezone.now)  # Timestamp of message

    # Room is optional and nullable to avoid migration issues
    room = models.CharField(max_length=100, blank=True, null=True)  # Chat room name (optional)

    def __str__(self):
        # Display username and first 20 characters of the message
        return f"{self.user.username}: {self.message[:20]}"


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique room name

    def __str__(self):
        return self.name
