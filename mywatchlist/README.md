# Tugas 3 PBP

### Perbedaan HTML, JSON, dan XML

1. HTML<br>
   HTML adalah singkatan dari _Hypertext Markup Language_, di mana HTML digunakan untuk menampilkan halaman-halaman web. Elemen-elemen statis (button, hyperlink, image, dan lain-lain) dan juga dinamis (data dari _database_) dapat ditampilkan pada halaman HTML. Untuk membuat halaman web dengan HTML, kita harus menggunakan format _tags_.

   Contoh dari halaman HTML sederhana adalah sebagai berikut:

   ```html
   <html>
     <head>
       <title>My Epic Website</title>
     </head>
     <body>
       <h1>Hey, this is an H1!</h1>
       <p>This is fun, isn't it?</p>
     </body>
   </html>
   ```

2. JSON<br>
   JSON adalah singkatan dari _JavaScript Object Notation_, di mana JSON menampung data-data aplikasi terkait dalam bentuk _key-value pair_. Data-data yang berbeda dipisah dengan karakter koma (`,`). Ukuran data pada JSON lebih kecil dibandingkan ukuran data yang ditampung dalam XML.

   Contoh dari JSON adalah sebagai berikut:

   ```json
   {
     "team_name": "Manchester United",
     "city": "Manchester",
     "league": "Premier League"
   }
   ```

   Suatu JSON bisa berupa _nested_, sebagai berikut:

   ```json
   {
     "name": "Andrew Johnson",
     "age": 21,
     "favorite_music": {
       "title": "Never Gonna Give You Up",
       "singer": "Rick Astley"
     }
   }
   ```

   Suatu atribut dalam JSON bisa berupa array, sebagai berikut:

   ```json
   {
     "name": "Andrew Johnson",
     "age": 21,
     "friends": [
       {
         "name": "Michael McKenny",
         "age": 21
       },
       {
         "name": "Susan Connor",
         "age": 22
       }
     ]
   }
   ```

3. XML<br>
   XML adalah singkatan dari _Extensible Markup Language_, di mana XML digunakan untuk melakukan _data-delivery_, seperti halnya JSON. Namun, hal yang membedakan antara XML dengan JSON adalah formatnya yang cukup serupa dengan HTML, di mana XML menggunakan _tags_ (contohnya `<firstname>Gibrano</firstname>`). Hal ini akan menyebabkan data yang ditampung menjadi lebih besar ukurannya dibandingkan JSON.

   Contoh dari _file_ XML sederhana adalah sebagai berikut:

   ```xml
   <store>
      <item>
         <name>Milk</name>
         <price>Rp20.000</price>
         <stock>50</stock>
      </item>
      <item>
         <name>Rice</name>
         <price>Rp25.000</price>
         <stock>200</stock>
      </item>
      <item>
         <name>Apple</name>
         <price>Rp10.000</price>
         <stock>30</stock>
      </item>
   </store>
   ```

### Pentingnya _Data-Delivery_ dalam Platform

_Data-delivery_ sangat esensial di dalam proses kerja platform, karena jika tidak ada mekanisme tersebut, maka data dari _database_ tidak bisa ditampilkan di sisi _frontend_. Misalnya, dalam membuat aplikasi pemberitahu cuaca, jika tidak ada sistem _data-delivery_ di dalam aplikasi tersebut, maka data terbaru mengenai cuaca di daerah tertentu tidak dapat ditampilkan pada sisi user dan tentunya, tujuan dari aplikasi tersebut tidak dapat tercapai.

### Implementasi Checklist Tugas 3

1. Membuat _app_ Django baru, yaitu `mywatchlist`<br>
   Untuk membuat _app_ baru, saya menjalankan command berikut:

   ```
   python manage.py startapp mywatchlist
   ```

2. Menambahkan _path_ `mywatchlist`<br>
   Untuk menambahkan _path_ baru, saya mengakses _file_ `urls.py` pada folder `project-django`, kemudian saya memodifikasi list `urlpatterns` sebagai berikut:

   ```py
   urlpatterns = [
    ...
    path('mywatchlist/', include('mywatchlist.urls')),
   ]
   ```

   Ketika ada user yang mengakses path `mywatchlist/`, _request_ tersebut akan di-_handle_ di dalam file `urls.py` yang ada pada folder `mywatchlist`, yang telah dibuat pada langkah 1.

3. Membuat model `MyWatchList`<br>
   Untuk membuat model baru, saya mengakses file `models.py` yang ada di dalam folder `mywatchlist`, kemudian saya menambahkan kode berikut:

   ```py
   class MyWatchList(models.Model):
      title = models.CharField(max_length=255)
      watched = models.BooleanField()
      rating = models.IntegerField()
      release_date = models.DateField()
      review = models.TextField()
   ```

   Ada beberapa pertimbangan ketika saya memilih _field_ yang digunakan untuk setiap atribut model tersebut:

   - `title`<br>
     Menurut saya, judul suatu film seharusnya tidak terlalu panjang, sehingga saya menggunakan `CharField` dengan menetapkan panjang maksimum 255 karakter.

   - `watched`<br>
     Menurut saya, karena data pada atribut ini adalah _ya_ atau _tidak_, maka saya memutuskan untuk menggunakan `BooleanField`, sehingga data yang tersimpan mudah dipahami (hanya berupa `true` atau `false`, atau sudah ditonton atau belum) dan, jika diinginkan, dapat dimanfaatkan untuk menambahkan informasi pada halaman HTML (berkaitan dengan bagian `bonus`).

   - `rating`<br>
     Karena rating yang akan digunakan hanya angka bulat 1 sampai 5, maka saya memutuskan untuk menggunakan `IntegerField` untuk atribut ini.

   - `release_date`<br>
     Karena berupa tanggal, saya memutuskan untuk menggunakan `DateField` untuk atribut ini. Menurut saya, hal ini akan memudahkan untuk _formatting_ tanggal dibandingkan menggunakan `CharField`.

   - `review`<br>
     Karena review cenderung berupa paragraf yang terdiri dari beberapa kalimat, maka saya memutuskan untuk memanfaatkan `TextField` pada atribut ini.

4. Menambahkan 10 data<br>
   Untuk menambahkan 10 data pada _database_, maka hal yang saya lakukan adalah membuat folder baru yang bernama `fixtures` di dalam folder `mywatchlist`, kemudian membuat file JSON baru yang bernama `initial_watchlist_data.json` di dalam folder tersebut. Kemudian saya menambahkan 10 data dengan format sebagai berikut:

   ```json
   [
    {
        "model": "mywatchlist.mywatchlist",
        "pk": 1,
        "fields": {
            "title": "Avengers: Endgame",
            "watched": true,
            "rating": 5,
            "release_date": "2019-04-24",
            "review": "This is the ultimate treat for Marvel fans who has been there since the beginning of the Marvel Cinematic Universe. Marvel fans can't miss this epic conclusion!"
        }
    },
    {
        "model": "mywatchlist.mywatchlist",
        "pk": 2,
        "fields": {
            "title": "Spider-Man: No Way Home",
            "watched": true,
            "rating": 5,
            "release_date": "2021-12-15",
            "review": "The fans' anticipation of this epic conclusion of the Spider-Man MCU trilogy will be well worth it. Watch it will fellow Spider-Man and/or MCU fans, get a popcorn, and experience a brilliant action-packed and heartfelt Spider-Man movie."
        }
    },
    ...
    ]
   ```

   Atribut masing-masing data disesuaikan dengan atribut yang ada di class `MyWatchList`.

5. Menyajikan data dalam format HTML, JSON, dan XML<br>
   Untuk membuat fitur ini, maka saya membuat 3 fungsi di `views.py` yang ada pada folder `mywatchlist` sebagai berikut:<br>

   `Untuk HTML`<br>

   ```py
   def show_watchlist_in_html(request):
      data = MyWatchList.objects.all()
      watched_count = MyWatchList.objects.filter(watched=True).count()
      not_watched_count = MyWatchList.objects.filter(watched=False).count()

      context = {
         "watchlist_data": data,
         "often_watch": True if watched_count >= not_watched_count else False
      }
      return render(request, "mywatchlist.html", context)
   ```

   Saya mengambil semua data watchlist yang ada di _database_, kemudian memasukkan ke dalam suatu dictionary `context`, dan memanggil fungsi `render()` dengan memasukkan `context` sebagai salah satu argumen fungsi tersebut.

   Untuk mengerjakan bagian bonus, saya menambahkan `often_watch` ke dalam dictionary `context`, di mana variabel tersebut memuat informasi apakah user lebih banyak menonton daripada belum menonton. Hal ini agar saya dapat menggunakan informasi ini untuk me-_render_ elemen yang sesuai dengan keterangan pada soal.

   Data pada `context` dapat saya gunakan pada `mywatchlist.html`, yang akan menjadi tempat di mana saya menyajikan data watchlist dengan HTML. Isi dari file tersebut adalah sebagai berikut:

   ```html
   {% extends 'base.html' %} {% block content %}
   <h1>My Watchlist</h1>

   <!-- Display message yang berbeda tergantung apakah user lebih sering menonton atau tidak -->
   {% if often_watch %}
   <h3>Selamat, kamu sudah banyak menonton!</h3>
   {% else %}
   <h3>Wah, kamu masih sedikit menonton!</h3>
   {% endif %}

   <!-- Iterasi semua data watchlist -->
   {% for data in watchlist_data %}
   <div>
     <h3>{{data.pk}}. {{data.title}}</h3>

     <strong>Watched</strong>
     <p>{{data.watched}}</p>

     <strong>Rating</strong>
     <p>{{data.rating}}</p>

     <strong>Release Date</strong>
     <!-- Formatting tanggal -->
     <p>{{data.release_date | date:"F j, Y"}}</p>

     <strong>Review</strong>
     <p>{{data.review}}</p>
     <hr />
   </div>
   {% endfor %} {% endblock content %}
   ```

   `Untuk JSON`<br>

   ```py
   def show_watchlist_in_json(request):
      data = MyWatchList.objects.all()
      return HttpResponse(serializers.serialize("json", data), content_type="application/json")
   ```

   Seperti view untuk HTML, saya juga mengambil semua data watchlist yang ada di _database_. Hal yang membedakan adalah saya tidak menggunakan fungsi `render()`, melainkan saya hanya mengembalikan suatu `HttpResponse` yang isinya adalah data watchlist dalam bentuk JSON.

   `Untuk XML`<br>

   ```py
   def show_watchlist_in_xml(request):
      data = MyWatchList.objects.all()
      return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
   ```

   Fungsi ini mirip dengan view untuk JSON, hanya saja _response_ yang akan diberikan adalah data watchlist dalam bentuk XML.

6. Membuat _routing_<br>
   Karena di langkah 2 saya sudah men-_state_ bahwa semua _route request_ user yang diawali dengan `mywatchlist/` akan di-_handle_ di dalam file `urls.py` yang ada di dalam folder `mywatchlist`, maka saya harus menambahkan 3 views yang telah dibuat pada langkah 5 ke dalam file tersebut.

   Berikut isi dari `urls.py` tersebut:

   ```py
   from django.urls import path
   from mywatchlist import views

   urlpatterns = [
      path("html/", views.show_watchlist_in_html, name="show_watchlist_in_html"),
      path("json/", views.show_watchlist_in_json, name="show_watchlist_in_json"),
      path("xml/", views.show_watchlist_in_xml, name="show_watchlist_in_xml")
   ]
   ```

   Terlihat bahwa:<br>

   - Jika user mengakses `mywatchlist/html/`, maka fungsi `show_watchlist_in_html()` pada file `views.py` milik `mywatchlist` akan dijalankan untuk meng-_handle_ _request_ tersebut.<br>
   - Jika user mengakses `mywatchlist/json/`, maka fungsi `show_watchlist_in_json()` pada file `views.py` milik `mywatchlist` akan dijalankan untuk meng-_handle_ _request_ tersebut.<br>
   - Jika user mengakses `mywatchlist/xml/`, maka fungsi `show_watchlist_in_xml()` pada file `views.py` milik `mywatchlist` akan dijalankan untuk meng-_handle_ _request_ tersebut.<br>

7. Melakukan _deployment_<br>
   Untuk melakukan _deployment_, karena saya menggunakan _repository_ dan _app_ Heroku yang sama dengan Tugas 2, maka saya melakukan perintah berikut:

   ```
   git add .
   git commit -m "(some commit message)"
   git push -u origin main
   ```

   Perubahan pada kode _repository_ ini akan mengubah pula _app_ Heroku yang terkait.

   Satu hal yang saya ubah adalah `HEROKU_APP_NAME` saya, karena saya mengubah nama _repository_ dan _app_ Heroku agar saya hanya menggunakan _repository_ ini untuk tugas-tugas PBP berikutnya.

### Pemeriksaan _Routes_ dengan Postman

1. `mywatchlist/html`<br><br>
   ![mywatchlist/html](https://user-images.githubusercontent.com/70869295/191177256-4a9698d9-0579-41bf-b510-fc541f92fa43.png)

2. `mywatchlist/json`<br><br>
   ![mywatchlist/json](https://user-images.githubusercontent.com/70869295/191177273-f4fe2c95-ac57-4548-bbd0-01562d0c1d28.png)

3. `mywatchlist/xml`<br><br>
   ![mywatchlist/xml](https://user-images.githubusercontent.com/70869295/191177316-bfd46a9e-813e-4d16-8d07-fd3a4bdde1f7.png)
