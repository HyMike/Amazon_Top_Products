from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("products_stats/", views.products_stats, name="products_stats"),

]
