from django.contrib import admin
from .models import Tag, Post, Subscriber


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "source_type", "author", "published_at", "is_featured")
    list_filter = ("source_type", "tags", "is_featured", "published_at")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)

    def get_changeform_initial_data(self, request):
        return {"source_type": "editorial", "author": "PyNews 팀"}


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)
