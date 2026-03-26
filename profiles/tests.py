from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class ProfileApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="profile-owner@example.com",
            username="profile-owner",
            password="strongpass123",
        )
        self.other_user = User.objects.create_user(
            email="profile-other@example.com",
            username="profile-other",
            password="strongpass123",
        )

    def test_profile_is_created_automatically(self):
        self.assertTrue(hasattr(self.user, "profile"))

    def test_authenticated_user_can_view_and_update_own_profile(self):
        self.client.force_authenticate(user=self.user)

        me_response = self.client.get("/api/profiles/me/")
        patch_response = self.client.patch(
            f"/api/profiles/{self.user.profile.pk}/",
            {"bio": "Updated bio", "location": "Kyiv"},
            format="json",
        )

        self.user.profile.refresh_from_db()

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.profile.bio, "Updated bio")
        self.assertEqual(self.user.profile.location, "Kyiv")

    def test_user_cannot_update_someone_elses_profile(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            f"/api/profiles/{self.user.profile.pk}/",
            {"bio": "Hacked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
