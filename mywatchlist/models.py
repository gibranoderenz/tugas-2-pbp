from django.db import models

# Create your models here.


class MyWatchList(models.Model):
    title = models.CharField(max_length=255)
    watched = models.BooleanField()
    rating = models.IntegerField()
    release_date = models.DateField()
    review = models.TextField()
