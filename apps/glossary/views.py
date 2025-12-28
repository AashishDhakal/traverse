"""Views for Glossary app."""
from django.views.generic import DetailView, ListView

from .models import Term


class TermListView(ListView):
    """List all glossary terms (A-Z)."""

    model = Term
    template_name = "glossary/term_list.html"
    context_object_name = "terms"

    def get_queryset(self):
        return Term.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Group terms by first letter
        terms_by_letter = {}
        for term in context["terms"]:
            letter = term.name[0].upper()
            if letter not in terms_by_letter:
                terms_by_letter[letter] = []
            terms_by_letter[letter].append(term)

        context["terms_by_letter"] = dict(sorted(terms_by_letter.items()))
        context["letters"] = list(context["terms_by_letter"].keys())

        return context


class TermDetailView(DetailView):
    """Glossary term detail page."""

    model = Term
    template_name = "glossary/term_detail.html"
    context_object_name = "term"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_terms"] = self.object.related_terms.all()[:6]
        context["related_trips"] = self.object.related_trips.filter(is_published=True)[:4]
        return context
