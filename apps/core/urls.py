"""URL configuration for Core app."""
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("tags/<slug:slug>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("destinations/", views.RegionListView.as_view(), name="region_list"),
    path("destinations/<slug:slug>/", views.RegionDetailView.as_view(), name="region_detail"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
