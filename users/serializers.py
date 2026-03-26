from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source="follower_relations.count",
        read_only=True
    )
    following_count = serializers.IntegerField(
        source="following_relations.count",
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "followers_count",
            "following_count",
        )
        read_only_fields = ("id", "followers_count", "following_count")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


UserCreateSerializer = UserSerializer
