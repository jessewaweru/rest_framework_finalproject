from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class NotificationViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    # the user will get the notifications that have not been read
    # def get_queryset(self):
    #     user = self.request.user
    #     return self.queryset.filter(user=user, is_read=False)

    # The user will get the notifications that have not been read
    def get_queryset(self):
        # Check if `self.request` is None (during schema generation)
        if self.request is None:
            return self.queryset.none()
        user = self.request.user
        return self.queryset.filter(user=user, is_read=False)

    @action(detail=True, methods=["post"])
    def marked_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})
