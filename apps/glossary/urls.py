"""URL configuration for Glossary app."""
from django.urls import path

from . import views

app_name = "glossary"

urlpatterns = [
    path("", views.TermListView.as_view(), name="term_list"),
    path("<slug:slug>/", views.TermDetailView.as_view(), name="term_detail"),
]
