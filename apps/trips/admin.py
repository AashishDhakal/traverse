"""Admin configuration for Trips app with Django Unfold and WYSIWYG."""
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Trip, TripGalleryImage


class TripAdminForm(forms.ModelForm):
    """Custom form with WYSIWYG editor for rich text fields."""

    class Meta:
        model = Trip
        fields = [
            "title",
            "slug",
            "tagline",
            "overview",
            "detailed_itinerary",
            "highlights",
            "includes",
            "excludes",
            "essential_info",
            "tags",
            "region",
            "trip_type",
            "duration_days",
            "max_altitude",
            "difficulty",
            "best_seasons",
            "group_size_min",
            "group_size_max",
            "price",
            "discounted_price",
            "featured_image",
            "video_url",
            "route_coordinates",
            "meta_title",
            "meta_description",
            "focus_keyword",
            "is_published",
            "is_featured",
        ]
        widgets = {
            "detailed_itinerary": WysiwygWidget(),
            "highlights": WysiwygWidget(),
            "includes": WysiwygWidget(),
            "excludes": WysiwygWidget(),
            "essential_info": WysiwygWidget(),
            "overview": WysiwygWidget(),
        }


class TripGalleryImageInline(TabularInline):
    """Inline admin for trip gallery images."""

    model = TripGalleryImage
    extra = 1
    fields = ["image", "caption", "alt_text", "display_order"]


@admin.register(Trip)
class TripAdmin(ModelAdmin):
    """Admin configuration for Trip model."""

    form = TripAdminForm

    list_display = [
        "title",
        "featured_thumbnail",
        "region",
        "difficulty",
        "duration_days",
        "price_display",
        "is_published",
        "is_featured",
    ]
    list_filter = ["is_published", "is_featured", "difficulty", "trip_type", "region"]
    search_fields = ["title", "slug", "overview", "tagline"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    list_editable = ["is_published", "is_featured"]
    inlines = [TripGalleryImageInline]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["title", "slug", "tagline", "overview", "trip_type"],
            },
        ),
        (
            "Taxonomy & Region",
            {
                "fields": ["tags", "region"],
            },
        ),
        (
            "Logistics",
            {
                "fields": [
                    ("duration_days", "max_altitude"),
                    ("difficulty", "best_seasons"),
                    ("group_size_min", "group_size_max"),
                ],
            },
        ),
        (
            "Pricing",
            {
                "fields": [("price", "discounted_price")],
            },
        ),
        (
            "Media",
            {
                "fields": ["featured_image", "video_url"],
            },
        ),
        (
            "Detailed Content",
            {
                "fields": [
                    "detailed_itinerary",
                    "highlights",
                    "includes",
                    "excludes",
                    "essential_info",
                ],
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
            "Helicopter Tour Details",
            {
                "fields": [
                    ("flight_duration_minutes", "helicopter_capacity"),
                    "departure_location",
                    "landing_sites",
                ],
                "classes": ["collapse"],
                "description": "Only applicable for Helicopter Tour trip type",
            },
        ),
        (
            "Publishing",
            {
                "fields": [("is_published", "is_featured")],
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

    @admin.display(description="Price")
    def price_display(self, obj):
        if obj.discounted_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">${}</span> <strong>${}</strong>',
                obj.price,
                obj.discounted_price,
            )
        return f"${obj.price}"


@admin.register(TripGalleryImage)
class TripGalleryImageAdmin(ModelAdmin):
    """Admin for managing gallery images."""

    list_display = ["trip", "image_thumbnail", "caption", "display_order"]
    list_filter = ["trip"]
    list_editable = ["display_order"]

    @admin.display(description="Preview")
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"
