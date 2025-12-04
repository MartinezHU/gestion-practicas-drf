from rest_framework import serializers
from apps.core.models import APIUser


class APIUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIUser
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "username",
            "password",
            "origin_app",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = APIUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
