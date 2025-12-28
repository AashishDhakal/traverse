"""
Content app - Marketing content layer.
Contains BlogPost model for content marketing.
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone


class BlogCategory(models.Model):
    """Optional hierarchical categories for blog posts."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    Content marketing posts.

    Unified Architecture: Uses ManyToMany to UniversalTag,
    enabling shared taxonomy with Trip.

    E-E-A-T: Links to TeamMember for author attribution.
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("published", "Published"),
    ]

    CONTENT_TYPE_CHOICES = [
        ("guide", "Travel Guide"),
        ("story", "Travel Story"),
        ("tips", "Tips & Advice"),
        ("news", "News & Updates"),
        ("gear", "Gear Reviews"),
        ("culture", "Culture & History"),
        ("safety", "Safety & Health"),
    ]

    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    excerpt = models.TextField(max_length=300, help_text="Brief summary for listings and social sharing")
    content = models.TextField(help_text="Main content (HTML supported)")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default="guide")

    # CONTENT INJECTION - Explicit trip links
    linked_trips = models.ManyToManyField(
        "trips.Trip",
        related_name="linked_by_blogs",
        blank=True,
        help_text="Trips to feature as recommendations in this post",
    )

    # UNIFIED ARCHITECTURE - Shared taxonomy
    related_tags = models.ManyToManyField(
        "core.UniversalTag",
        related_name="blogposts",
        blank=True,
        help_text="Tags for categorization (shared with trips)",
    )
    region = models.ForeignKey(
        "core.Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        help_text="Geographic region context",
    )
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")

    # E-E-A-T: Author attribution
    author = models.ForeignKey(
        "team.TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        help_text="Author for E-E-A-T compliance",
    )

    # Media
    featured_image = models.ImageField(
        upload_to="blog/featured/", blank=True, help_text="Featured image (recommended: 1200x630)"
    )

    # SEO
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (defaults to post title)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (defaults to excerpt)")
    focus_keyword = models.CharField(max_length=100, blank=True, help_text="Primary keyword for SEO optimization")

    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False, help_text="Feature on homepage or section headers")
    published_at = models.DateTimeField(null=True, blank=True)

    # Analytics
    view_count = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-published_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate meta fields
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]

        # Set published_at on first publish
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:post_detail", kwargs={"slug": self.slug})

    @property
    def read_time_minutes(self):
        """Estimate reading time based on word count."""
        word_count = len(self.content.split())
        return max(1, word_count // 200)

    def get_recommended_trips(self, limit=3):
        """
        Get trips to recommend at end of article.

        Priority:
        1. Explicitly linked trips
        2. Fallback: Trips sharing same tags
        """
        explicit = self.linked_trips.filter(is_published=True)

        if explicit.exists():
            return explicit[:limit]

        # Fallback: find trips with same tags
        from apps.trips.models import Trip

        return Trip.objects.filter(tags__in=self.related_tags.all(), is_published=True).distinct()[:limit]

    def get_related_posts(self, limit=4):
        """Get related blog posts based on tags."""
        return (
            BlogPost.objects.filter(related_tags__in=self.related_tags.all(), status="published")
            .exclude(id=self.id)
            .distinct()[:limit]
        )

    def increment_views(self):
        """Thread-safe view count increment."""
        BlogPost.objects.filter(pk=self.pk).update(view_count=models.F("view_count") + 1)
