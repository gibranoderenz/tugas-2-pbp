from django.urls import path
from katalog import views

urlpatterns = [
    path("", views.get_catalog_items, name="get_catalog_items")
]
