from django.contrib import admin

from posts.models import Hashtag, Post


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at", "updated_at")
    search_fields = ("author__email", "author__username", "content")
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("author",)
    filter_horizontal = ("hashtags",)
