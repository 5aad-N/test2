"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import main_spa
from . import api_views

urlpatterns = [
    # SPA entry point (server-rendered shell)
    path("", main_spa, name="main_spa"),

    # REST API endpoints
    path("api/csrf/", api_views.api_csrf, name="api_csrf"),
    path("api/auth/signup/", api_views.api_signup, name="api_signup"),
    path("api/auth/login/", api_views.api_login, name="api_login"),
    path("api/auth/logout/", api_views.api_logout, name="api_logout"),
    path("api/auth/me/", api_views.api_get_user, name="api_get_user"),
    path("api/profile/", api_views.api_update_profile, name="api_update_profile"),

    # Item/Auction endpoints
    path("api/items/", api_views.api_items, name="api_items"),
    path("api/items/<int:item_id>/", api_views.api_item_detail, name="api_item_detail"),
    path("api/items/<int:item_id>/edit/", api_views.api_update_item, name="api_update_item"),
    path("api/items/<int:item_id>/delete/", api_views.api_delete_item, name="api_delete_item"),
    path("api/items/<int:item_id>/bid/", api_views.api_place_bid, name="api_place_bid"),
    path("api/items/<int:item_id>/questions/", api_views.api_ask_question, name="api_ask_question"),
    path("api/questions/<int:question_id>/answer/", api_views.api_answer_question, name="api_answer_question"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)