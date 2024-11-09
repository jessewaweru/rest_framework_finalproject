from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.


class NotificationViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    # the user will get the notifications that have not been read
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user, is_read=False)

    def marked_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})
