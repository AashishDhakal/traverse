"""Admin configuration for Core app with Django Unfold."""
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Region, UniversalTag


@admin.register(UniversalTag)
class UniversalTagAdmin(ModelAdmin):
    """Admin configuration for UniversalTag model."""

    list_display = [
        "name",
        "slug",
        "icon",
        "is_featured",
        "get_trip_count",
        "get_blog_count",
        "display_order",
    ]
    list_filter = ["is_featured"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_featured", "display_order"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "slug", "icon", "description"],
            },
        ),
        (
            "SEO",
            {
                "fields": ["meta_title", "meta_description"],
                "classes": ["collapse"],
            },
        ),
        (
            "Display",
            {
                "fields": ["is_featured", "display_order"],
            },
        ),
    ]

    @admin.display(description="Trips")
    def get_trip_count(self, obj):
        count = obj.trips.count()
        return format_html('<span style="color: #0d9488; font-weight: 600;">{}</span>', count)

    @admin.display(description="Blogs")
    def get_blog_count(self, obj):
        count = obj.blogposts.count()
        return format_html('<span style="color: #7c3aed; font-weight: 600;">{}</span>', count)


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    """Admin configuration for Region model."""

    list_display = [
        "name",
        "slug",
        "parent",
        "is_featured",
        "get_trip_count",
        "display_order",
    ]
    list_filter = ["is_featured", "parent"]
    search_fields = ["name", "slug", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_featured", "display_order"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "slug", "parent", "description"],
            },
        ),
        (
            "Media",
            {
                "fields": ["featured_image"],
            },
        ),
        (
            "Location",
            {
                "fields": [("latitude", "longitude")],
                "classes": ["collapse"],
            },
        ),
        (
            "SEO",
            {
                "fields": ["meta_title", "meta_description"],
                "classes": ["collapse"],
            },
        ),
        (
            "Display",
            {
                "fields": ["is_featured", "display_order"],
            },
        ),
    ]

    @admin.display(description="Trips")
    def get_trip_count(self, obj):
        count = obj.trips.count()
        return format_html('<span style="color: #0d9488; font-weight: 600;">{}</span>', count)
