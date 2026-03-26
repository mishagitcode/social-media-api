from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from interactions.models import Comment, Like
from interactions.tasks import get_post_engagement
from posts.models import Post


User = get_user_model()


class InteractionApiTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            email="post-author@example.com",
            username="post-author",
            password="strongpass123",
        )
        self.user = User.objects.create_user(
            email="interaction-user@example.com",
            username="interaction-user",
            password="strongpass123",
        )
        self.post = Post.objects.create(author=self.author, content="Test post")
        self.client.force_authenticate(user=self.user)

    def test_user_can_like_post_only_once(self):
        first_response = self.client.post(
            "/api/likes/",
            {"post": self.post.pk},
            format="json",
        )
        second_response = self.client.post(
            "/api/likes/",
            {"post": self.post.pk},
            format="json",
        )

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)

    def test_user_can_create_comment(self):
        response = self.client.post(
            "/api/comments/",
            {"post": self.post.pk, "content": "Nice post"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.user).exists())

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_TASK_EAGER_PROPAGATES=True,
    )
    def test_celery_engagement_task_returns_post_metrics(self):
        Like.objects.create(user=self.user, post=self.post)
        Comment.objects.create(author=self.user, post=self.post, content="Nice post")

        result = get_post_engagement.delay(self.post.pk).get()

        self.assertEqual(
            result,
            {
                "post_id": self.post.pk,
                "likes_count": 1,
                "comments_count": 1,
            },
        )
