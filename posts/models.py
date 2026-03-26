from django.conf import settings
from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post #{self.pk} by {self.author}"