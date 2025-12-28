"""
Core app - Universal taxonomy layer.
Contains UniversalTag and Region models that bind content together.
"""
from django.db import models
from django.urls import reverse


class UniversalTag(models.Model):
    """
    Universal taxonomy binding Trips and BlogPosts together.

    The Master Tag System - used by both Trip and BlogPost models
    to create topical authority and internal linking power.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome or Heroicon class (e.g., 'fa-mountain')")
    description = models.TextField(blank=True, help_text="SEO-optimized description for tag landing pages")

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True, help_text="Custom title for search engines (max 70 chars)")
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="Meta description for search engines (max 160 chars)"
    )

    # Ordering
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Universal Tag"
        verbose_name_plural = "Universal Tags"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:tag_detail", kwargs={"slug": self.slug})

    def get_related_content(self):
        """
        Fetch both trips and blogs for this tag.

        Returns a dict with:
        - 'trips': QuerySet of published Trip objects
        - 'blogs': QuerySet of published BlogPost objects
        """
        return {
            "trips": self.trips.filter(is_published=True).select_related("region"),
            "blogs": self.blogposts.filter(status="published").select_related("author"),
        }

    def get_trip_count(self):
        """Return count of published trips with this tag."""
        return self.trips.filter(is_published=True).count()

    def get_blog_count(self):
        """Return count of published blog posts with this tag."""
        return self.blogposts.filter(status="published").count()


class Region(models.Model):
    """
    Hierarchical regions for geographic organization.

    Examples: Nepal > Everest Region > Khumbu Valley
    Supports unlimited nesting depth.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")

    description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to="regions/", blank=True, help_text="Hero image for region landing page")

    # Geographic coordinates for maps
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Ordering
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_absolute_url(self):
        return reverse("core:region_detail", kwargs={"slug": self.slug})

    def get_ancestors(self):
        """Return list of ancestor regions from root to parent."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors

    def get_descendants(self):
        """Return all descendant regions (recursive)."""
        descendants = list(self.children.all())
        for child in self.children.all():
            descendants.extend(child.get_descendants())
        return descendants

    def get_all_trips(self):
        """Get trips from this region and all sub-regions."""
        from apps.trips.models import Trip

        region_ids = [self.id] + [r.id for r in self.get_descendants()]
        return Trip.objects.filter(region_id__in=region_ids, is_published=True)


class SiteConfiguration(models.Model):
    """
    Per-site branding and configuration for multi-portal support.

    Allows running multiple travel portals from a single codebase:
    - Traverse The Himalayas
    - VisitNepalDirect
    - NepalLuxe
    - BudgetHimalaya
    """

    site = models.OneToOneField(
        "sites.Site",
        on_delete=models.CASCADE,
        related_name="configuration",
    )

    # Branding
    brand_name = models.CharField(max_length=100, help_text="Display name (e.g., 'Traverse The Himalayas')")
    tagline = models.CharField(max_length=200, blank=True, help_text="Short marketing tagline")
    logo = models.ImageField(upload_to="sites/logos/", help_text="Main logo (recommended: 200x60)")
    logo_light = models.ImageField(upload_to="sites/logos/", blank=True, help_text="Light version for dark backgrounds")
    favicon = models.ImageField(upload_to="sites/favicons/", blank=True)

    # Theme colors (hex format)
    primary_color = models.CharField(max_length=7, default="#0369a1", help_text="Primary brand color (hex)")
    secondary_color = models.CharField(max_length=7, default="#0f766e", help_text="Secondary brand color (hex)")
    accent_color = models.CharField(max_length=7, default="#f59e0b", help_text="Accent/CTA color (hex)")

    # Market segment
    SEGMENT_CHOICES = [
        ("general", "General"),
        ("luxury", "Luxury"),
        ("budget", "Budget"),
        ("adventure", "Adventure"),
    ]
    target_segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES, default="general")

    # SEO
    meta_description = models.CharField(max_length=160, help_text="Default meta description for the site")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")

    # Contact
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    # Footer
    footer_text = models.TextField(blank=True, help_text="Additional footer text/disclaimer")
    footer_description = models.TextField(blank=True, help_text="Footer brand description (shown below logo)")
    copyright_name = models.CharField(max_length=100, blank=True, help_text="Copyright holder name")

    # Hero Section
    hero_title = models.CharField(max_length=100, blank=True, help_text="Homepage hero title (e.g., 'Discover Nepal')")
    hero_subtitle = models.TextField(blank=True, help_text="Homepage hero subtitle/description")
    hero_cta_text = models.CharField(
        max_length=50, default="Explore Trips", help_text="Hero call-to-action button text"
    )
    hero_image = models.ImageField(upload_to="sites/hero/", blank=True, help_text="Homepage hero background")

    # Page Titles
    title_suffix = models.CharField(
        max_length=50, blank=True, help_text="Suffix for page titles (e.g., ' | NepalLuxe')"
    )

    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="GA4 Measurement ID")
    facebook_pixel_id = models.CharField(max_length=50, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configurations"

    def __str__(self):
        return f"{self.brand_name} ({self.site.domain})"

    @classmethod
    def get_current(cls, request=None):
        """Get configuration for current site."""
        from django.contrib.sites.models import Site

        if request and hasattr(request, "site_config"):
            return request.site_config

        try:
            current_site = Site.objects.get_current()
            return cls.objects.select_related("site").get(site=current_site)
        except cls.DoesNotExist:
            return None
