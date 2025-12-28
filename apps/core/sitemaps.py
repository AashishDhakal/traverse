"""
Dynamic Sitemaps for SEO.

Auto-generates sitemap.xml for Trips, Blogs, Tags, Regions, and Glossary terms.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.content.models import BlogPost
from apps.core.models import Region, UniversalTag
from apps.glossary.models import Term
from apps.team.models import TeamMember
from apps.trips.models import Trip


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""

    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["core:home", "core:contact", "core:tag_list", "core:region_list"]

    def location(self, item):
        return reverse(item)


class TripSitemap(Sitemap):
    """Sitemap for Trip pages - highest priority for product pages."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Trip.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class BlogPostSitemap(Sitemap):
    """Sitemap for Blog posts - high priority for content marketing."""

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class TagSitemap(Sitemap):
    """Sitemap for Tag hub pages - topical authority builders."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return UniversalTag.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class RegionSitemap(Sitemap):
    """Sitemap for Region pages."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Region.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class GlossarySitemap(Sitemap):
    """Sitemap for Glossary term pages - SEO internal linking power."""

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Term.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class TeamMemberSitemap(Sitemap):
    """Sitemap for Team member pages - E-E-A-T author pages."""

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return TeamMember.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


# Sitemap dictionary for urls.py
sitemaps = {
    "static": StaticViewSitemap,
    "trips": TripSitemap,
    "blog": BlogPostSitemap,
    "tags": TagSitemap,
    "regions": RegionSitemap,
    "glossary": GlossarySitemap,
    "team": TeamMemberSitemap,
}
