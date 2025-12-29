"""
Site configuration middleware for multi-portal support.

Detects the current site from the request domain and attaches
the SiteConfiguration to the request object.
"""
from django.contrib.sites.models import Site
from django.core.cache import cache


class SiteConfigurationMiddleware:
    """
    Middleware that attaches site configuration to every request.

    Sets request.site and request.site_config based on the domain.
    Falls back to SITE_ID setting if domain not found.
    """

    CACHE_TIMEOUT = 300  # 5 minutes

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.http import HttpResponse

        # Get site configuration for this request
        request.site, request.site_config = self._get_site_config(request)

        # Check if site is disabled (but allow admin access)
        if (
            request.site_config
            and not getattr(request.site_config, "is_active", True)
            and not request.path.startswith("/admin")
        ):
            return HttpResponse(
                self._get_maintenance_page(request.site_config),
                status=503,
                content_type="text/html",
            )

        response = self.get_response(request)
        return response

    def _get_maintenance_page(self, config):
        """Return a simple maintenance page HTML."""
        brand = config.brand_name if config else "Site"
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{brand} - Maintenance</title>
            <style>
                body {{ font-family: system-ui, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: linear-gradient(135deg, #1e293b, #0f172a); color: white; }}
                .container {{ text-align: center; padding: 2rem; }}
                h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
                p {{ color: #94a3b8; font-size: 1.25rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏔️ {brand}</h1>
                <p>We're currently performing maintenance. Please check back soon.</p>
            </div>
        </body>
        </html>
        """

    def _get_site_config(self, request):
        """Get Site and SiteConfiguration for the current request."""
        from apps.core.models import SiteConfiguration

        host = request.get_host().split(":")[0]  # Remove port if present
        cache_key = f"site_config:{host}"

        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Try to find site by domain
        site = None
        try:
            site = Site.objects.get(domain=host)
        except Site.DoesNotExist:
            # Try without www prefix
            if host.startswith("www."):
                try:
                    site = Site.objects.get(domain=host[4:])
                except Site.DoesNotExist:
                    pass

            # Fall back to current site based on SITE_ID, or first site
            if site is None:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    site = Site.objects.first()  # Last resort fallback

        # Get configuration for this site
        try:
            config = SiteConfiguration.objects.select_related("site").get(site=site)
        except SiteConfiguration.DoesNotExist:
            config = None

        result = (site, config)
        cache.set(cache_key, result, self.CACHE_TIMEOUT)
        return result
