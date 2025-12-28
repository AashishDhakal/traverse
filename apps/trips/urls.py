"""URL configuration for Trips app."""
from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.TripListView.as_view(), name="trip_list"),
    path("<slug:slug>/", views.TripDetailView.as_view(), name="trip_detail"),
]
