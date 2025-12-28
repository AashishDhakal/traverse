"""Views for Trips app."""
from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Trip


class TripListView(ListView):
    """List all published trips."""

    model = Trip
    template_name = "trips/trip_list.html"
    context_object_name = "trips"
    paginate_by = 12

    def get_queryset(self):
        queryset = Trip.objects.filter(is_published=True).select_related("region")

        # Filter by tag
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Filter by region
        region_slug = self.request.GET.get("region")
        if region_slug:
            queryset = queryset.filter(region__slug=region_slug)

        # Filter by difficulty
        difficulty = self.request.GET.get("difficulty")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        # Filter by duration
        duration = self.request.GET.get("duration")
        if duration:
            if duration == "1-7":
                queryset = queryset.filter(duration_days__lte=7)
            elif duration == "8-14":
                queryset = queryset.filter(duration_days__gte=8, duration_days__lte=14)
            elif duration == "15+":
                queryset = queryset.filter(duration_days__gte=15)

        # Search
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(overview__icontains=search) | Q(tagline__icontains=search)
            )

        # Sorting
        sort = self.request.GET.get("sort", "-is_featured")
        if sort == "price_low":
            queryset = queryset.order_by("price")
        elif sort == "price_high":
            queryset = queryset.order_by("-price")
        elif sort == "duration":
            queryset = queryset.order_by("duration_days")
        else:
            queryset = queryset.order_by("-is_featured", "-created_at")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.core.models import Region, UniversalTag

        context["tags"] = UniversalTag.objects.all()[:20]
        context["regions"] = Region.objects.filter(parent__isnull=True)[:10]
        context["difficulties"] = Trip.DIFFICULTY_CHOICES
        return context


class TripDetailView(DetailView):
    """Trip detail page."""

    model = Trip
    template_name = "trips/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self):
        return Trip.objects.filter(is_published=True).select_related("region")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related guides (Read Before You Go)
        context["related_guides"] = self.object.related_guides

        # Similar trips
        context["similar_trips"] = self.object.get_similar_trips(4)

        return context
