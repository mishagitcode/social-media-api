from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from config.permissions import IsOwnerOrReadOnly
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    owner_field = "user"

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)
