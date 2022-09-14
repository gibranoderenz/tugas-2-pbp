# Tugas 2 PBP

Link hasil _deployment_ tugas ini dapat diakses [di sini](https://gibs-tugas-2-pbp.herokuapp.com/katalog/).

## Proses _Request_ dan _Response_

### Bagan

![Bagan Request-Response Tugas 2 PBP](https://user-images.githubusercontent.com/70869295/189836526-d7899933-6c75-4275-9802-3150d6153bb6.png)

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

## Proses Pengerjaan Tugas 2

### 1. Membuat fungsi di `views.py`<br>

Untuk membuat fungsi yang dapat mengambil data dari model, saya meng-_assign_ suatu variabel, yaitu `catalog_items`, untuk menampung semua _item_ catalog. Variabel tersebut saya isi dengan `CatalogItem.objects.all()`
yang akan mengembalikan semua object `CatalogItem` yang ada di _database_.

Data tersebut dimasukkan ke dalam suatu dictionary `context` yang akan menjadi salah satu argumen dalam fungsi `render()`. Hal ini untuk mengirimkan data-data tersebut ke `katalog.html` yang nantinya akan di-_render_.

### 2. Membuat routing untuk fungsi tersebut<br>

Untuk setup routing fungsi tersebut, hal pertama yang saya lakukan adalah memodifikasi list `urlpatterns` pada `project-django/urls.py` menjadi sebagai berikut:

```py
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', include('example_app.urls')),
 path('katalog/', include('katalog.urls')),
]
```

Kemudian saya mengisi file `katalog/urls.py` dengan kode berikut:

```py
from django.urls import path
from katalog import views

urlpatterns = [
   path("", views.get_catalog_items, name="get_catalog_items")
]
```

Maka, _route_ `katalog/` akan berfungsi dengan semestinya.

### 3. Memetakan data ke HTML<br>

Untuk ini, saya memodifikasi file `katalog.html` sebagai berikut:

```html
<h5>Name:</h5>
<p>{{ name }}</p>

<h5>Student ID:</h5>
<p>{{ student_ID }}</p>
```

Bagian di atas akan men-_display_ value dari key `name` dan `student_ID` yang diperoleh dari dictionary `context` yang disajikan dari fungsi awal di `views.py`.

```html
<table>
  ... {% comment %} Add the data below this line {% endcomment %} {% for item in
  catalog_items %}
  <tr>
    <th>{{ item.item_name }}</th>
    <th>{{ item.item_price }}</th>
    <th>{{ item.item_stock }}</th>
    <th>{{ item.rating }}</th>
    <th>{{ item.description }}</th>
    <th><a href="{{" item.item_url }}> {{ item.item_name }} </a></th>
  </tr>
  {% endfor %}
</table>
```

Bagian di atas akan menampilkan semua atribut yang dimiliki masing-masing objek `CatalogItem` yang ada di dalam _database_. Hal ini juga dimungkinkan dengan menggunakan sintaks Django Template Language, pada kasus ini dengan _for-loop_.

### 4. Melakukan _deployment_<br>

Hal pertama yang saya lakukan adalah membuat app Heroku baru. Saya beri nama `gibs-tugas-2-pbp`. Kemudian, saya menyimpan nama app tersebut ke Actions Secrets _repository_ GitHub akan akan menampung _project_ ini dengan nama `HEROKU_APP_NAME`. Kemudian, saya juga menyimpan API Key akun Heroku saya ke dalam `Actions Secrets` _repository_ GitHub yang sama, tetapi kali ini dengan nama `HEROKU_API_KEY`. Akhirnya, saya _re-run_ _workflows_ yang ada di tab `Actions` _repository_ GitHub, dan situs web tersebut berjalan.
