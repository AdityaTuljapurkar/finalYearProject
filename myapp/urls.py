from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)



urlpatterns = [
    path("create-room/",views.MessageCreateView.as_view() , name='create-room'),
    path('room/', include(router.urls)),
 
]