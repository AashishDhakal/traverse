"""Views for Team app."""
from django.views.generic import DetailView, ListView

from .models import TeamMember


class MemberListView(ListView):
    """List all team members."""

    model = TeamMember
    template_name = "team/member_list.html"
    context_object_name = "members"

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True).order_by("display_order", "name")


class MemberDetailView(DetailView):
    """Team member detail page - Author page for E-E-A-T."""

    model = TeamMember
    template_name = "team/member_detail.html"
    context_object_name = "member"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.get_published_posts()[:10]
        context["expertise_tags"] = self.object.get_expertise_tags()
        return context
