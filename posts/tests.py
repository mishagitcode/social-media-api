from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post


User = get_user_model()


class PostApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="post-owner@example.com",
            username="post-owner",
            password="strongpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_post_normalizes_hashtags(self):
        payload = {
            "content": "Post with hashtags",
            "hashtags": [{"name": "#Django"}, {"name": "API"}],
        }

        response = self.client.post("/api/posts/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(pk=response.data["id"])
        self.assertEqual(
            set(post.hashtags.values_list("name", flat=True)),
            {"django", "api"},
        )

    def test_can_filter_posts_by_hashtag(self):
        first_post = Post.objects.create(author=self.user, content="First")
        first_post.hashtags.create(name="django")
        second_post = Post.objects.create(author=self.user, content="Second")
        second_post.hashtags.create(name="python")

        response = self.client.get("/api/posts/?hashtag=django")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], first_post.id)
