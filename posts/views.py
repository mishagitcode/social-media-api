from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from config.permissions import IsOwnerOrReadOnly
from posts.models import Hashtag, Post
from posts.serializers import HashtagSerializer, PostSerializer


class HashtagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hashtag.objects.all().order_by("name")
    serializer_class = HashtagSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name.lstrip("#").lower())
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related(
        "hashtags",
        "likes",
        "comments",
    )
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    owner_field = "author"

    def get_queryset(self):
        queryset = self.queryset
        author_id = self.request.query_params.get("author")
        hashtag = self.request.query_params.get("hashtag")

        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if hashtag:
            queryset = queryset.filter(
                hashtags__name__iexact=hashtag.lstrip("#").lower()
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
