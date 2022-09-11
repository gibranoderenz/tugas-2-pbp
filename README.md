# Tugas 2 PBP

Link hasil _deployment_ tugas ini dapat diakses [di sini](https://gibs-tugas-2-pbp.herokuapp.com/katalog/).

## Proses _Request_ dan _Response_

### Bagan

```
ada bagan di sini







```

### Penjelasan

1. URL ke `urls.py`<br>
   Saat user mengakses [link ini](https://gibs-tugas-2-pbp.herokuapp.com/katalog/), Django akan pergi ke file `urls.py` pada folder utama (yaitu folder project), kemudian akan mencari route `katalog/` pada list `urlpatterns`.

2. Di `urls.py`<br>
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

3. `katalog/urls.py` ke `views.py`<br>
   Setelah ...

## Mengapa Menggunakan _Virtual Environment_?

Dengan menggunakan _virtual environment_ saat mengerjakan proyek Django, _dependencies_ proyek tersebut tidak akan mengganggu Python yang sudah di-_install_ secara global di _device_ dan menjadikan _workspace_ pengerjaan proyek lebih bersih.

## Proses Pengerjaan Tugas Ini

text goes here
