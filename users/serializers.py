from rest_framework import serializers
from .models import User
from schools.validators import validate_rating
from .models import UserProfile
from .models import Review
from .models import History
from .utils import send_otp_email

""" This serializer is used to update and create a user and their User profile together"""


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "city", "county", "location"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "user_type",
            "is_school",
            "profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password")  # Extract password
        user = User.objects.create_user(**validated_data)  # Use create_user method
        user.set_password(password)  # Hash the password
        user.save()
        if not user.is_school:
            UserProfile.objects.create(user=user, **profile_data)

        send_otp_email(user)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        if not instance.is_school:
            UserProfile.objects.update_or_create(user=instance, defaults=profile_data)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(validators=[validate_rating])

    class Meta:
        model = Review
        fields = ["user", "school", "comment", "rating", "created_at"]


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ["school", "viewed_at"]
