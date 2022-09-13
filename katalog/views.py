from django.shortcuts import render
from .models import CatalogItem

def get_catalog_items(request):
    catalog_items = CatalogItem.objects.all()
    context = {
        "name": "Gibrano Fabien Derenz",
        "student_ID": "2106750622",
        "catalog_items": catalog_items
    }
    return render(request, "katalog.html", context)
