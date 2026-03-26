from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "birth_date", "created_at")
    search_fields = ("user__email", "user__username", "location")
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("user",)
