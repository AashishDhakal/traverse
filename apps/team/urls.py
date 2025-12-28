"""URL configuration for Team app."""
from django.urls import path

from . import views

app_name = "team"

urlpatterns = [
    path("", views.MemberListView.as_view(), name="member_list"),
    path("<slug:slug>/", views.MemberDetailView.as_view(), name="member_detail"),
]
