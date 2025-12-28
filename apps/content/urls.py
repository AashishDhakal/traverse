"""URL configuration for Content app."""
from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
