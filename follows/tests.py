from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from follows.models import Follow


User = get_user_model()


class FollowApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="follow-user@example.com",
            username="follow-user",
            password="strongpass123",
        )
        self.other_user = User.objects.create_user(
            email="follow-target@example.com",
            username="follow-target",
            password="strongpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_follow_another_user(self):
        response = self.client.post(
            "/api/follows/",
            {"following": self.other_user.pk},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        follow = Follow.objects.get()
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.following, self.other_user)

    def test_user_cannot_follow_themself(self):
        response = self.client.post(
            "/api/follows/",
            {"following": self.user.pk},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 0)
