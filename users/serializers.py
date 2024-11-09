from rest_framework import serializers
from .models import User, Review
from schools.validators import validate_rating
from .models import UserProfile

""" This serializer is used to update and create a user and their User profile together"""


class UserProfileSerializer(serializers.ModelSerializer):
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
            "profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        UserProfile.objects.update_or_create(user=instance, defaults="profile_data")


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(validators=[validate_rating])

    class Meta:
        model = Review
        fields = ["user", "school", "comment", "rating", "created_at"]
