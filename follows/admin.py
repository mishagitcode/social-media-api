from django.contrib import admin

from follows.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")
    search_fields = (
        "follower__email",
        "follower__username",
        "following__email",
        "following__username",
    )
    list_filter = ("created_at",)
    raw_id_fields = ("follower", "following")
