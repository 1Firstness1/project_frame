"""Главная страница и общий HTML-каркас проекта."""

from django.http import HttpResponse

BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title, content):
    """Собрать HTML-страницу с единым каркасом и навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP}">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">Сервис гостей</a>
        <div class="navbar-nav">
            <a class="nav-link" href="/">Главная</a>
            <a class="nav-link" href="/events/">События</a>
            <a class="nav-link" href="/guests/">Гости</a>
            <a class="nav-link" href="/invitations/">Приглашения</a>
        </div>
    </div>
</nav>
<main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница проекта."""
    content = """
    <h1 class="display-4">Сервис управления списком гостей</h1>
    <p class="lead">Учёт событий, гостей и приглашений.</p>
    <p>Основные разделы:</p>
    <a href="/events/" class="btn btn-primary me-2">События</a>
    <a href="/guests/" class="btn btn-secondary me-2">Гости</a>
    <a href="/invitations/" class="btn btn-success">Приглашения</a>
    """
    return HttpResponse(page("Сервис гостей", content))


def page_not_found(request, exception):
    """Пользовательская страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )