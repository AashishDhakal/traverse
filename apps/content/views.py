"""Views for Content app."""
from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import BlogCategory, BlogPost


class PostListView(ListView):
    """List all published blog posts."""

    model = BlogPost
    template_name = "content/post_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status="published").select_related("author", "region")

        # Filter by tag
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            queryset = queryset.filter(related_tags__slug=tag_slug)

        # Filter by content type
        content_type = self.request.GET.get("type")
        if content_type:
            queryset = queryset.filter(content_type=content_type)

        # Filter by author
        author_slug = self.request.GET.get("author")
        if author_slug:
            queryset = queryset.filter(author__slug=author_slug)

        # Search
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(excerpt__icontains=search) | Q(content__icontains=search)
            )

        return queryset.distinct().order_by("-is_featured", "-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.core.models import UniversalTag

        context["tags"] = UniversalTag.objects.filter(blogposts__status="published").distinct()[:15]
        context["content_types"] = BlogPost.CONTENT_TYPE_CHOICES
        return context


class PostDetailView(DetailView):
    """Blog post detail page."""

    model = BlogPost
    template_name = "content/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status="published").select_related("author", "region")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recommended trips (explicit > tag-based)
        context["recommended_trips"] = self.object.get_recommended_trips()

        # Related posts
        context["related_posts"] = self.object.get_related_posts(4)

        return context


class CategoryDetailView(DetailView):
    """Blog category page."""

    model = BlogCategory
    template_name = "content/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: Add posts filtering by category
        return context
