from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from follows.models import Follow


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )
    follower_email = serializers.EmailField(source="follower.email", read_only=True)
    following_email = serializers.EmailField(
        source="following.email",
        read_only=True
    )

    class Meta:
        model = Follow
        fields = (
            "id",
            "follower",
            "follower_email",
            "following",
            "following_email",
            "created_at",
        )
        read_only_fields = (
            "id",
            "follower_email",
            "following_email",
            "created_at",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("follower", "following"),
                message="You already follow this user.",
            )
        ]

    def validate(self, attrs):
        follower = attrs.get("follower", getattr(self.instance, "follower", None))
        following = attrs.get("following", getattr(self.instance, "following", None))

        if follower and following and follower == following:
            raise serializers.ValidationError(
                {"following": "You cannot follow yourself."}
            )

        return attrs
