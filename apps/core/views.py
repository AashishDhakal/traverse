"""Views for Core app."""
from django.db.models import Count
from django.views.generic import DetailView, ListView, TemplateView

from .models import Region, UniversalTag


class HomeView(TemplateView):
    """Homepage view."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured trips
        from apps.trips.models import Trip

        context["featured_trips"] = Trip.objects.filter(is_published=True, is_featured=True).select_related("region")[
            :6
        ]

        # Latest blog posts
        from apps.content.models import BlogPost

        context["latest_posts"] = BlogPost.objects.filter(status="published").select_related("author")[:3]

        # Featured regions
        context["featured_regions"] = Region.objects.filter(is_featured=True)[:4]

        # Featured tags
        context["featured_tags"] = UniversalTag.objects.filter(is_featured=True)[:8]

        return context


class TagListView(ListView):
    """List all tags."""

    model = UniversalTag
    template_name = "core/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return UniversalTag.objects.annotate(
            trip_count=Count("trips", distinct=True), blog_count=Count("blogposts", distinct=True)
        ).order_by("display_order", "name")


class TagDetailView(DetailView):
    """Tag detail page - Topic Hub."""

    model = UniversalTag
    template_name = "core/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get related content using the unified method
        context["content"] = self.object.get_related_content()

        # Get related tags (tags that share trips or blogs)
        related_tag_ids = set()
        for trip in context["content"]["trips"][:5]:
            related_tag_ids.update(trip.tags.values_list("id", flat=True))
        for blog in context["content"]["blogs"][:5]:
            related_tag_ids.update(blog.related_tags.values_list("id", flat=True))
        related_tag_ids.discard(self.object.id)

        context["related_tags"] = UniversalTag.objects.filter(id__in=list(related_tag_ids)[:8])

        return context


class RegionListView(ListView):
    """List all regions."""

    model = Region
    template_name = "core/region_list.html"
    context_object_name = "regions"

    def get_queryset(self):
        # Only top-level regions
        return Region.objects.filter(parent__isnull=True).order_by("display_order", "name")


class RegionDetailView(DetailView):
    """Region detail page."""

    model = Region
    template_name = "core/region_detail.html"
    context_object_name = "region"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trips"] = self.object.get_all_trips()[:6]
        context["sub_regions"] = self.object.children.all()
        context["ancestors"] = self.object.get_ancestors()

        from apps.content.models import BlogPost

        context["posts"] = BlogPost.objects.filter(region=self.object, status="published").select_related("author")[:5]

        return context


class ContactView(TemplateView):
    """Contact page."""

    template_name = "core/contact.html"
