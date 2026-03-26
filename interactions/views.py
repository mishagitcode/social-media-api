from rest_framework import mixins, permissions, viewsets

from config.permissions import IsOwnerOrReadOnly
from interactions.models import Comment, Like
from interactions.serializers import CommentSerializer, LikeSerializer


class LikeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Like.objects.select_related("user", "post", "post__author").all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    owner_field = "user"

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user")
        post_id = self.request.query_params.get("post")

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post", "post__author").all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    owner_field = "author"

    def get_queryset(self):
        queryset = self.queryset
        post_id = self.request.query_params.get("post")
        author_id = self.request.query_params.get("author")

        if post_id:
            queryset = queryset.filter(post_id=post_id)
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
