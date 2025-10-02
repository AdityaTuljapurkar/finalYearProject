from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import UserSerializer, MessageSerializer
from .models import Room
from .serializers import RoomSerializer
from rest_framework import viewsets
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow anyone to sign up

class MessageCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Only logged in users allowed

    def get_queryset(self):
        # Filter messages by room, room name passed as query param in URL
        return Message.objects.filter(room=self.request.query_params.get('room'))

    def perform_create(self, serializer):
        # Save the new message with user from request and room from posted data
        serializer.save(user=self.request.user, room=self.request.data.get('room'))

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]  