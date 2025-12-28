"""Admin configuration for Team app with Django Unfold."""
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    """Admin for TeamMember with E-E-A-T focus."""

    list_display = [
        "photo_thumbnail",
        "name",
        "role",
        "title",
        "is_verified_expert",
        "years_experience",
        "is_active",
    ]
    list_filter = ["role", "is_verified_expert", "is_active"]
    search_fields = ["name", "bio", "title"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_verified_expert", "is_active"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "slug", "role", "title", "photo"],
            },
        ),
        (
            "Biography",
            {
                "fields": ["short_bio", "bio"],
            },
        ),
        (
            "Expertise (E-E-A-T)",
            {
                "fields": [
                    "certifications",
                    ("years_experience", "trips_led", "summits"),
                    "is_verified_expert",
                ],
            },
        ),
        (
            "Social Links",
            {
                "fields": ["social_links"],
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
            "Status",
            {
                "fields": ["is_active", "display_order"],
            },
        ),
    ]

    @admin.display(description="Photo")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;" />',
                obj.photo.url,
            )
        return format_html(
            '<div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #0d9488, #7c3aed); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{}</div>',
            obj.name[0].upper() if obj.name else "?",
        )
