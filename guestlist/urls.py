"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("events/", include("events.urls")),
    path("guests/", include("guests.urls")),
    path("invitations/", include("invitations.urls")),
]

handler404 = "homepage.views.page_not_found"