from celery import shared_task

from posts.models import Post


@shared_task
def get_post_engagement(post_id):
    post = Post.objects.get(pk=post_id)
    return {
        "post_id": post.pk,
        "likes_count": post.likes.count(),
        "comments_count": post.comments.count(),
    }
