"""
Team app - Authority layer for Google E-E-A-T compliance.
Contains TeamMember model for expert authors and guides.
"""
from django.conf import settings
from django.db import models
from django.urls import reverse


class TeamMember(models.Model):
    """
    Expert authors/guides for E-E-A-T compliance.

    Every blog post shows a "Verified Expert" author card
    to satisfy Google's quality guidelines.
    """

    ROLE_CHOICES = [
        ("guide", "Mountain Guide"),
        ("author", "Content Writer"),
        ("expert", "Subject Matter Expert"),
        ("founder", "Founder"),
    ]

    # Link to Django user (optional)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Optional link to user account for login",
    )

    # Basic info
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="author")
    title = models.CharField(max_length=100, blank=True, help_text="Professional title (e.g., 'Senior Trek Leader')")

    # Bio and credibility
    bio = models.TextField(help_text="Full biography for author page")
    short_bio = models.CharField(max_length=200, blank=True, help_text="One-liner for author cards on blog posts")
    photo = models.ImageField(upload_to="team/")

    # Certifications for credibility (E-E-A-T)
    certifications = models.JSONField(
        default=list,
        blank=True,
        help_text='List of certifications, e.g., ["Certified Wilderness First Responder", "IFMGA Guide"]',
    )

    # Social proof
    social_links = models.JSONField(
        default=dict, blank=True, help_text='Social links, e.g., {"linkedin": "url", "instagram": "url"}'
    )

    # Experience metrics
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience in the industry")
    trips_led = models.PositiveIntegerField(default=0, help_text="Number of trips/expeditions led")
    summits = models.PositiveIntegerField(default=0, help_text="Number of successful summits")

    # Verification status
    is_verified_expert = models.BooleanField(default=False, help_text="Display 'Verified Expert' badge on posts")
    is_active = models.BooleanField(default=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Ordering
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def get_absolute_url(self):
        return reverse("team:member_detail", kwargs={"slug": self.slug})

    def get_published_posts(self):
        """Return all published blog posts by this author."""
        return self.authored_posts.filter(status="published")

    def get_post_count(self):
        """Return count of published posts."""
        return self.get_published_posts().count()

    def get_expertise_tags(self):
        """Return unique tags from all authored posts."""
        from apps.core.models import UniversalTag

        return UniversalTag.objects.filter(blogposts__author=self, blogposts__status="published").distinct()
