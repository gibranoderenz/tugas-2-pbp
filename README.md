# Tugas 2 PBP

Link hasil _deployment_ tugas ini dapat diakses [di sini](https://gibs-tugas-2-pbp.herokuapp.com/katalog/).

## Proses _Request_ dan _Response_

### Bagan

```
ada bagan di sini







```

### Penjelasan

1. **URL ke `urls.py`<br>**
   Saat user mengakses [link ini](https://gibs-tugas-2-pbp.herokuapp.com/katalog/), Django akan pergi ke file `urls.py` pada folder utama (yaitu folder project), kemudian akan mencari route `katalog/` pada list `urlpatterns`.

2. **Di `urls.py`<br>**
   Perlu diingat struktur `urlpatterns`:

   ```py
   urlpatterns = [
     path("admin/", admin.site.urls),
     path("", include("example_app.urls")),
     path("katalog/", include("katalog.urls")),
   ]
   ```

   Perhatikan kode berikut:

   ```py
   ...
   path("katalog/", include("katalog.urls")),
   ...
   ```

   Kode tersebut berarti _setiap request user untuk mengakses route `katalog` akan di-handle oleh file katalog/urls.py_. Hal ini, menurut saya, untuk merapikan struktur kode proyek Django.

3. **`katalog/urls.py` ke `views.py`**<br>
   Django kemudian akan mencari file `urls.py` di folder `katalog`, kemudian mencari _route_ `/`, karena route awal adalah `katalog/`.

   ```py
   from django.urls import path
   from katalog import views


   urlpatterns = [
      path("", views.get_catalog_items, name="get_catalog_items")
   ]
   ```

   Terlihat bahwa _route_ tersebut di-_handle_ oleh salah satu _view_ yang terdapat di `katalog/views`, yaitu `get_catalog_items`.

4. **Di `views.py`**<br>
   Seperti yang telah dijabarkan sebelumnya, fungsi `get_catalog_items` akan menjadi _request handler_ dari `katalog/`.

   ```py
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
   ```

   Terlihat bahwa fungsi tersebut akan me-_render_ suatu halaman HTML, pada kasus ini adalah `katalog.html`, serta diberikan context yang dapat di-_render_ di halaman HTML tersebut. Dengan kata lain, fungsi tersebut akan mengembalikan halaman HTML sebagai _response_ dari _request_ user, yaitu `katalog/`.

   Tetapi tidak hanya sebatas itu saja interaksi yang terjadi di `get_catalog_items`. Perhatikan kode berikut:

   ```py
   catalog_items = CatalogItem.objects.all()
   ```

   Di sini, `get_catalog_items` juga berinteraksi dengan _model_ `CatalogItem`, pada kasus ini untuk mengambil semua benda katalog yang ada di dalam _database_, dengan tujuan untuk men-_display_ data tersebut di halaman HTML `katalog.html`.

5. **Halaman HTML disajikan**<br>
   Akhirnya, user dapat mengakses halaman HTML, yaitu `katalog.html`.

## Mengapa Menggunakan _Virtual Environment_?

Dengan menggunakan _virtual environment_ saat mengerjakan proyek Django, _dependencies_ proyek tersebut tidak akan mengganggu Python yang sudah di-_install_ secara global di _device_ dan menjadikan _workspace_ pengerjaan proyek lebih bersih.

Selain itu, _virtual environment_ ini memungkinkan project Django yang sedang dikerjakan dijalankan di laptop atau PC lain. Misalnya, peserta A dalam suatu kelompok memiliki _repository project_ Django. Kemudian, peserta B melakukan _cloning_ terhadap _repo_ tersebut. Agar semua _dependencies_ project tersebut dapat dimiliki oleh _device_ B, maka ia akan melakukan `pip install -r requirements.txt`. Hal ini akan menunjang agar _project_ Django yang ada di _device_ A bisa sama dengan yang dimiliki di _device_ B.

## Proses Pengerjaan Tugas Ini

text goes here
