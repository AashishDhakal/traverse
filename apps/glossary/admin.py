"""Admin configuration for Glossary app with Django Unfold and WYSIWYG."""
from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Term


class TermAdminForm(forms.ModelForm):
    """Custom form with WYSIWYG editor for detailed explanation."""

    class Meta:
        model = Term
        fields = [
            "name",
            "slug",
            "abbreviation",
            "definition",
            "detailed_explanation",
            "related_terms",
            "related_trips",
            "related_tags",
            "auto_link",
            "link_priority",
            "max_links_per_page",
            "meta_title",
            "meta_description",
        ]
        widgets = {
            "detailed_explanation": WysiwygWidget(),
        }


@admin.register(Term)
class TermAdmin(ModelAdmin):
    """Admin for glossary terms."""

    form = TermAdminForm

    list_display = [
        "name",
        "abbreviation",
        "auto_link",
        "link_priority",
        "max_links_per_page",
    ]
    list_filter = ["auto_link"]
    search_fields = ["name", "abbreviation", "definition"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["related_terms", "related_trips", "related_tags"]
    list_editable = ["auto_link", "link_priority"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "slug", "abbreviation"],
            },
        ),
        (
            "Definition",
            {
                "fields": ["definition", "detailed_explanation"],
            },
        ),
        (
            "Related Content",
            {
                "fields": ["related_terms", "related_trips", "related_tags"],
            },
        ),
        (
            "Auto-Linking Settings",
            {
                "fields": [("auto_link", "link_priority", "max_links_per_page")],
            },
        ),
        (
            "SEO",
            {
                "fields": ["meta_title", "meta_description"],
                "classes": ["collapse"],
            },
        ),
    ]
