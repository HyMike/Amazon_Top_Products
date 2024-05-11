"""
URL configuration for the app.

This module defines the URL patterns for the app. It contains mappings between
URL paths and view functions or classes that handle HTTP requests.
"""

from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("products_trends/", views.products_trends, name="products_trends"),

]
