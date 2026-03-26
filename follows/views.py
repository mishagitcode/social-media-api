from rest_framework import mixins, permissions, viewsets

from config.permissions import IsOwnerOrReadOnly
from follows.models import Follow
from follows.serializers import FollowSerializer


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Follow.objects.select_related("follower", "following").all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    owner_field = "follower"

    def get_queryset(self):
        queryset = self.queryset
        follower_id = self.request.query_params.get("follower")
        following_id = self.request.query_params.get("following")

        if follower_id:
            queryset = queryset.filter(follower_id=follower_id)
        if following_id:
            queryset = queryset.filter(following_id=following_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
