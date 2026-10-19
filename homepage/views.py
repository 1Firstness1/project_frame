"""Главная страница и обработчик 404."""

from django.shortcuts import render


def index(request):
    """Главная страница проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Пользовательская страница ошибки 404."""
    return render(request, "404.html", status=404)
