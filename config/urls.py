"""
URL configuration for SummitX-Django project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    # Sitemap for SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # App URLs
    path("", include("apps.core.urls", namespace="core")),
    path("trips/", include("apps.trips.urls", namespace="trips")),
    path("blog/", include("apps.content.urls", namespace="content")),
    path("team/", include("apps.team.urls", namespace="team")),
    path("glossary/", include("apps.glossary.urls", namespace="glossary")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Traverse Administration"
admin.site.site_title = "Traverse Admin"
admin.site.index_title = "Traverse Dashboard"
