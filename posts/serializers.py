from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Hashtag, Post


User = get_user_model()


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")
        read_only_fields = ("id",)

    def validate_name(self, value):
        normalized_value = value.lstrip("#").strip().lower()

        if not normalized_value:
            raise serializers.ValidationError("Hashtag name cannot be blank.")

        return normalized_value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault(),
    )
    author_email = serializers.EmailField(source="author.email", read_only=True)
    hashtags = HashtagSerializer(many=True, required=False)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_email",
            "content",
            "image",
            "hashtags",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "author_email",
            "likes_count",
            "comments_count",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        hashtags_data = validated_data.pop("hashtags", [])
        post = Post.objects.create(**validated_data)
        self._save_hashtags(post, hashtags_data)
        return post

    def update(self, instance, validated_data):
        hashtags_data = validated_data.pop("hashtags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if hashtags_data is not None:
            self._save_hashtags(instance, hashtags_data)

        return instance

    def _save_hashtags(self, post, hashtags_data):
        hashtags = []
        for hashtag_data in hashtags_data:
            serializer = HashtagSerializer(data=hashtag_data)
            serializer.is_valid(raise_exception=True)
            hashtag, _ = Hashtag.objects.get_or_create(
                name=serializer.validated_data["name"]
            )
            hashtags.append(hashtag)

        post.hashtags.set(hashtags)


PostDetailSerializer = PostSerializer
