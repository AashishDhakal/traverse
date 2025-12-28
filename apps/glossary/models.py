"""
Glossary app - SEO glossary terms.
Contains Term model for auto-linking within blog content.
"""
from django.db import models
from django.urls import reverse


class Term(models.Model):
    """
    SEO Glossary terms for internal linking.

    These terms can be auto-linked in blog content via middleware,
    creating a powerful internal linking structure.
    """

    # Basic information
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True, db_index=True)
    abbreviation = models.CharField(
        max_length=20, blank=True, help_text="Short form (e.g., 'AMS' for 'Acute Mountain Sickness')"
    )

    # Definitions
    definition = models.TextField(help_text="Brief definition (shown in tooltips and listings)")
    detailed_explanation = models.TextField(blank=True, help_text="Detailed explanation (HTML supported)")

    # Related content
    related_terms = models.ManyToManyField("self", symmetrical=True, blank=True, help_text="Related glossary terms")
    related_trips = models.ManyToManyField(
        "trips.Trip", related_name="glossary_terms", blank=True, help_text="Trips where this term is relevant"
    )
    related_tags = models.ManyToManyField(
        "core.UniversalTag", related_name="glossary_terms", blank=True, help_text="Related topic tags"
    )

    # Auto-linking configuration
    auto_link = models.BooleanField(default=True, help_text="Automatically link this term in blog content")
    link_priority = models.PositiveIntegerField(default=5, help_text="Higher priority terms are linked first (1-10)")
    max_links_per_page = models.PositiveIntegerField(default=3, help_text="Maximum times to link this term per page")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Glossary Term"
        verbose_name_plural = "Glossary Terms"

    def __str__(self):
        if self.abbreviation:
            return f"{self.name} ({self.abbreviation})"
        return self.name

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = f"{self.name} - Trekking Glossary"[:70]
        if not self.meta_description:
            self.meta_description = self.definition[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("glossary:term_detail", kwargs={"slug": self.slug})
