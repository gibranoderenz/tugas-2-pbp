from django.urls import path
from mywatchlist import views

urlpatterns = [
    path("", views.index, name="index"),
    path("html/", views.show_watchlist_in_html, name="index"),
    path("json/", views.show_watchlist_in_json, name="show_watchlist_in_json"),
    path("xml/", views.show_watchlist_in_xml, name="show_watchlist_in_xml")
]
