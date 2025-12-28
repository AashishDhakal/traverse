"""Admin configuration for Content app with Django Unfold and WYSIWYG."""
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import BlogCategory, BlogPost


class BlogPostAdminForm(forms.ModelForm):
    """Custom form with WYSIWYG editor for content."""

    class Meta:
        model = BlogPost
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "content_type",
            "linked_trips",
            "related_tags",
            "region",
            "category",
            "author",
            "featured_image",
            "meta_title",
            "meta_description",
            "focus_keyword",
            "status",
            "is_featured",
            "published_at",
        ]
        widgets = {
            "content": WysiwygWidget(),
            "excerpt": WysiwygWidget(),
        }


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    """Admin configuration for BlogPost model."""

    form = BlogPostAdminForm

    list_display = [
        "title",
        "featured_thumbnail",
        "author",
        "content_type",
        "status",
        "is_featured",
        "published_at",
    ]
    list_filter = ["status", "content_type", "is_featured", "author"]
    search_fields = ["title", "slug", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["linked_trips", "related_tags"]
    list_editable = ["status", "is_featured"]
    date_hierarchy = "published_at"

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["title", "slug", "excerpt", "content_type"],
            },
        ),
        (
            "Content",
            {
                "fields": ["content", "featured_image"],
            },
        ),
        (
            "Author & Attribution",
            {
                "fields": ["author", "region"],
            },
        ),
        (
            "Content Injection (Trips)",
            {
                "fields": ["linked_trips"],
                "description": "Link trips to show as recommendations in this post.",
            },
        ),
        (
            "Taxonomy",
            {
                "fields": ["related_tags", "category"],
            },
        ),
        (
            "SEO",
            {
                "fields": ["meta_title", "meta_description", "focus_keyword"],
                "classes": ["collapse"],
            },
        ),
        (
            "Publishing",
            {
                "fields": [("status", "is_featured"), "published_at"],
            },
        ),
    ]

    @admin.display(description="Image")
    def featured_thumbnail(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url,
            )
        return "-"


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    """Admin for blog categories."""

    list_display = ["name", "slug", "parent"]
    prepopulated_fields = {"slug": ("name",)}
