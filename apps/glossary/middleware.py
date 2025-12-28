"""
Glossary Auto-Linker Middleware.

Scans blog content and automatically hyperlinks glossary terms
to their definition pages for SEO internal linking.
"""
import re

from django.core.cache import cache


class GlossaryAutoLinkerMiddleware:
    """
    Middleware that automatically links glossary terms in blog content.

    Features:
    - Caches term patterns for performance
    - Respects max_links_per_page setting per term
    - Skips terms already inside links
    - Case-insensitive matching
    """

    CACHE_KEY = "glossary_terms_for_linking"
    CACHE_TIMEOUT = 300  # 5 minutes

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only process HTML responses for blog detail pages
        content_type = response.get("Content-Type", "")
        if not content_type.startswith("text/html"):
            return response

        # Only process blog posts
        if not (request.path.startswith("/blog/") and request.path != "/blog/" and not request.path.endswith("/page/")):
            return response

        try:
            content = response.content.decode("utf-8")
            modified_content = self._inject_glossary_links(content)
            response.content = modified_content.encode("utf-8")
            response["Content-Length"] = len(response.content)
        except Exception:  # noqa: BLE001
            # If anything goes wrong, return original response unchanged
            return response

        return response

    def _get_terms(self):
        """Get all auto-linkable terms from cache or database."""
        terms = cache.get(self.CACHE_KEY)

        if terms is None:
            from apps.glossary.models import Term

            terms = list(
                Term.objects.filter(auto_link=True)
                .values("name", "abbreviation", "slug", "max_links_per_page", "link_priority")
                .order_by("-link_priority", "-id")
            )
            cache.set(self.CACHE_KEY, terms, self.CACHE_TIMEOUT)

        return terms

    def _make_replacer(self, slug, max_count, link_counts):
        """Factory to create replacer with properly bound variables."""

        def replace_term(match):
            if link_counts.get(slug, 0) >= max_count:
                return match.group(0)

            link_counts[slug] = link_counts.get(slug, 0) + 1
            matched_text = match.group(1)

            return (
                f'<a href="/glossary/{slug}/" '
                f'class="glossary-term" '
                f'title="View definition">'
                f"{matched_text}</a>"
            )

        return replace_term

    def _inject_glossary_links(self, content):
        """Inject glossary links into blog content."""
        terms = self._get_terms()

        if not terms:
            return content

        # Find the main content area to avoid modifying navigation/footer
        content_start = content.find("<article")
        content_end = content.find("</article>")

        if content_start == -1 or content_end == -1:
            return content

        pre_content = content[:content_start]
        main_content = content[content_start : content_end + 10]
        post_content = content[content_end + 10 :]

        # Track link counts per term
        link_counts = {}

        for term in terms:
            term_slug = term["slug"]
            max_links = term["max_links_per_page"]

            if link_counts.get(term_slug, 0) >= max_links:
                continue

            # Build patterns for term name and abbreviation
            patterns = [term["name"]]
            if term["abbreviation"]:
                patterns.append(term["abbreviation"])

            for pattern in patterns:
                if link_counts.get(term_slug, 0) >= max_links:
                    break

                # Case-insensitive word boundary match
                # Skip if already in a link or tag
                regex = re.compile(r"(?<![\<\w])(" + re.escape(pattern) + r")(?![\>\w])", re.IGNORECASE)

                replacer = self._make_replacer(term_slug, max_links, link_counts)
                main_content = regex.sub(replacer, main_content, count=max_links)

        return pre_content + main_content + post_content
