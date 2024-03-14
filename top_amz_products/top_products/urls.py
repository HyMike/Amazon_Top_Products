from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # to enable path for scrapping

    path("", views.home, name="home"),
    path("scraping_data/", views.scraping_data, name="scraping_data"),
    # may rename the function to something else.
    path("products_stats/", views.products_stats, name="products_stats"),
    path("category/", views.scrape_category, name='scrape_category'),

]
