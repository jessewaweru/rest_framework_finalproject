from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

# from .permissions import IsStaffOrAccOwner

# from .mixins import IsStaffPermissionMixin


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsStaffOrAccOwner]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete_related_data()
        self.perform_destroy(user)
        return Response(
            {"message": "Your account and data has been successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
