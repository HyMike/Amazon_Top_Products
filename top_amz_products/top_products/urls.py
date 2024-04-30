from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("products_trends/", views.products_trends, name="products_trends"),

]
