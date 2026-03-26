from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "username",
            "email",
            "bio",
            "avatar",
            "location",
            "birth_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "username",
            "email",
            "created_at",
            "updated_at",
        )
