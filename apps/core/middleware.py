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
        # Get site configuration for this request
        request.site, request.site_config = self._get_site_config(request)

        response = self.get_response(request)
        return response

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
        try:
            site = Site.objects.get(domain=host)
        except Site.DoesNotExist:
            # Try without www prefix
            if host.startswith("www."):
                try:
                    site = Site.objects.get(domain=host[4:])
                except Site.DoesNotExist:
                    site = Site.objects.get_current()
            else:
                # Fall back to current site based on SITE_ID
                site = Site.objects.get_current()

        # Get configuration for this site
        try:
            config = SiteConfiguration.objects.select_related("site").get(site=site)
        except SiteConfiguration.DoesNotExist:
            config = None

        result = (site, config)
        cache.set(cache_key, result, self.CACHE_TIMEOUT)
        return result
