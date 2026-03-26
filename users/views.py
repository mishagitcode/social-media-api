from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    owner_field = "self"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permission() for permission in self.permission_classes]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
