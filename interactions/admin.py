from django.contrib import admin

from interactions.models import Comment, Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    search_fields = ("user__email", "user__username", "post__content")
    list_filter = ("created_at",)
    raw_id_fields = ("user", "post")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at", "updated_at")
    search_fields = ("author__email", "author__username", "content")
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("author", "post")
