from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # to enable path for scrapping

    path("", views.categories, name="categories"),
    path("scraping_data/", views.scraping_data, name="scraping_data"),

]
