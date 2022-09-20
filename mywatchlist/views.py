from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import MyWatchList

# Create your views here.


def show_watchlist_in_html(request):
    data = MyWatchList.objects.all()
    watched_count = MyWatchList.objects.filter(watched=True).count()
    not_watched_count = MyWatchList.objects.filter(watched=False).count()

    context = {
        "watchlist_data": data,
        "often_watch": True if watched_count >= not_watched_count else False
    }
    return render(request, "mywatchlist.html", context)


def show_watchlist_in_json(request):
    data = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_watchlist_in_xml(request):
    data = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
