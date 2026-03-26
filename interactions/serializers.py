from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from interactions.models import Comment, Like
from posts.models import Post


User = get_user_model()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )
    user_email = serializers.EmailField(source="user.email", read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ("id", "user", "user_email", "post", "created_at")
        read_only_fields = ("id", "user_email", "created_at")
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=("user", "post"),
                message="You have already liked this post.",
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )
    author_email = serializers.EmailField(source="author.email", read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "author_email",
            "post",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author_email", "created_at", "updated_at")
