from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserApiTests(APITestCase):
    def test_user_registration_hashes_password(self):
        payload = {
            "email": "new-user@example.com",
            "username": "new-user",
            "password": "strongpass123",
        }

        response = self.client.post("/api/users/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.get(email=payload["email"])
        self.assertTrue(created_user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_jwt_obtain_refresh_and_authenticated_request(self):
        user = User.objects.create_user(
            email="jwt-user@example.com",
            username="jwt-user",
            password="strongpass123",
        )

        response = self.client.post(
            "/api/token/",
            {"email": user.email, "password": "strongpass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh_response = self.client.post(
            "/api/token/refresh/",
            {"refresh": response.data["refresh"]},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )
        me_response = self.client.get("/api/users/me/")

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["email"], user.email)
