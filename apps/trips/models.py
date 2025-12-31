"""
Trips app - Product layer.
Contains Trip model representing trekking/expedition packages.
"""
from django.db import models
from django.urls import reverse


class Trip(models.Model):
    """
    The core product - trekking/expedition packages.

    Unified Architecture: Uses ManyToMany to UniversalTag,
    enabling shared taxonomy with BlogPost.
    """

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("challenging", "Challenging"),
        ("extreme", "Extreme"),
    ]

    TRIP_TYPE_CHOICES = [
        ("trek", "Trekking"),
        ("expedition", "Expedition"),
        ("tour", "Tour"),
        ("climbing", "Peak Climbing"),
        ("helicopter", "Helicopter Tour"),
    ]

    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    tagline = models.CharField(
        max_length=200, blank=True, help_text="Short selling point (e.g., 'The ultimate Himalayan adventure')"
    )
    overview = models.TextField(help_text="Brief introduction shown at the top")

    # Rich content (Using standard TextField - Unfold provides editor widgets)
    detailed_itinerary = models.TextField(help_text="Day-by-day itinerary with rich formatting (HTML supported)")
    highlights = models.TextField(blank=True, help_text="Key highlights and unique selling points")
    includes = models.TextField(blank=True, help_text="What's included in the package")
    excludes = models.TextField(blank=True, help_text="What's not included")
    essential_info = models.TextField(blank=True, help_text="Important information, gear list, etc.")

    # UNIFIED ARCHITECTURE - Shared taxonomy
    tags = models.ManyToManyField(
        "core.UniversalTag", related_name="trips", blank=True, help_text="Tags for categorization and internal linking"
    )
    region = models.ForeignKey(
        "core.Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trips",
        help_text="Geographic region",
    )
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES, default="trek")

    # Logistics
    duration_days = models.PositiveIntegerField(help_text="Total duration in days")
    max_altitude = models.PositiveIntegerField(help_text="Maximum altitude in meters")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    best_seasons = models.JSONField(default=list, blank=True, help_text='e.g., ["spring", "autumn"]')
    group_size_min = models.PositiveIntegerField(default=1)
    group_size_max = models.PositiveIntegerField(default=15)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price in USD")
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Sale price (leave blank if no discount)"
    )

    # Media
    featured_image = models.ImageField(
        upload_to="trips/featured/", blank=True, null=True, help_text="Main hero image (recommended: 1920x1080)"
    )
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo embed URL")

    # Map data
    route_coordinates = models.JSONField(default=list, blank=True, help_text="GeoJSON coordinates for route map")

    # Helicopter-specific fields (only used when trip_type="helicopter")
    flight_duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Total flight time in minutes"
    )
    landing_sites = models.TextField(blank=True, help_text="Landing locations (e.g., 'Kalapatthar, Everest Base Camp')")
    helicopter_capacity = models.PositiveIntegerField(
        null=True, blank=True, default=5, help_text="Maximum passengers per helicopter"
    )
    departure_location = models.CharField(max_length=100, blank=True, default="Kathmandu", help_text="Departure point")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (defaults to trip title)")
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="SEO description (defaults to overview excerpt)"
    )
    focus_keyword = models.CharField(max_length=100, blank=True, help_text="Primary keyword for SEO optimization")

    # Publishing
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage featured section")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.overview[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("trips:trip_detail", kwargs={"slug": self.slug})

    @property
    def current_price(self):
        """Return discounted price if available, else base price."""
        return self.discounted_price or self.price

    @property
    def discount_percentage(self):
        """Calculate discount percentage if discounted."""
        if self.discounted_price and self.discounted_price < self.price:
            return int(((self.price - self.discounted_price) / self.price) * 100)
        return 0

    @property
    def related_guides(self):
        """
        Get blog posts related to this trip.

        Priority:
        1. Explicitly linked blog posts (via linked_trips M2M)
        2. Fallback: Posts sharing same tags
        """
        # Explicit links from BlogPost.linked_trips
        explicit = self.linked_by_blogs.filter(status="published")

        if explicit.exists():
            return explicit.select_related("author")[:5]

        # Fallback: find blogs with same tags
        from apps.content.models import BlogPost

        return (
            BlogPost.objects.filter(related_tags__in=self.tags.all(), status="published")
            .distinct()
            .select_related("author")[:5]
        )

    def get_similar_trips(self, limit=4):
        """Get similar trips based on shared tags and region."""
        similar = Trip.objects.filter(is_published=True).exclude(id=self.id)

        # Prioritize same region
        if self.region:
            similar = similar.filter(models.Q(region=self.region) | models.Q(tags__in=self.tags.all()))
        else:
            similar = similar.filter(tags__in=self.tags.all())

        return similar.distinct()[:limit]


class TripGalleryImage(models.Model):
    """
    Gallery images for Trip detail pages.
    Allows multiple images per trip with ordering.
    """

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="trips/gallery/", help_text="Gallery image (recommended: 1200x800)")
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility and SEO")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return f"{self.trip.title} - Image {self.display_order}"
