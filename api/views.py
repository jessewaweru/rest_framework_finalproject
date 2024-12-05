from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsStaffOrAccOwner

# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import action
# from users.models import OTP


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrAccOwner]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete_related_data()
        self.perform_destroy(user)
        return Response(
            {"message": "Your account and data has been successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # @action(detail=False, methods=["post"], url_path="verify-email")
    # def verify_email(self, request):
    #     email = request.data.get("email")
    #     otp_code = request.data.get("otp")

    #     user = get_object_or_404(User, email=email)

    #     try:
    #         otp = OTP.objects.get(user=user)
    #     except OTP.DoesNotExist:
    #         return Response(
    #             {"error": "OTP not found"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if not otp.is_valid():
    #         otp.delete()
    #         return Response(
    #             {"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if otp.code != otp_code:
    #         return Response(
    #             {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     user.email_verified = True
    #     user.is_active = True
    #     user.save()
    #     otp.delete()

    #     return Response(
    #         {"message": "Email verified successfully and account is now active"},
    #         status=status.HTTP_200_OK,
    #     )
