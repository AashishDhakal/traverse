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
