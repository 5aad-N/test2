from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Main SPA entry point. Serves the Vue application shell.
    Authentication checks are handled by Vue router.
    """
    user_context = None

    if request.user.is_authenticated:
        user_context = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "date_of_birth": str(request.user.date_of_birth) if request.user.date_of_birth else None,
            "profile_image": request.user.profile_image.url if request.user.profile_image else None
        }

    return render(request, "api/spa/index.html", {
        "user_data": user_context
    })
