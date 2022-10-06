# Tugas 4 dan 5 PBP

### Link

Tugas ini dapat diakses melalui link [berikut](https://gibs-tugas-pbp.herokuapp.com/todolist).

### Kegunaan `{% csrf_token %}` pada `<form>`

CSRF atau _Cross-Site Request Forgery_ adalah suatu _attack_ yang dilakukan terhadap seseorang **yang sudah terautentikasi** ke suatu website, di mana pengguna tersebut akan dibuat sang _hacker_ melakukan hal yang ia tidak maksud (misalnya, membayar sejumlah uang kepada _hacker_). Hal ini mungkin karena _session_ user di website yang terkait masih aktif, sehingga seolah-olah user benar-benar melakukan _request_ tersebut.

Terkait dengan submisi form, contoh dari _attack_ ini adalah sebagai berikut:

```html
<form action="http://bank.com/transfer.do" method="POST">
  <input type="hidden" name="acct" value="MARIA" />
  <input type="hidden" name="amount" value="100000" />
  <input type="submit" value="View my pictures" />
</form>
```

_(Sumber: https://owasp.org/www-community/attacks/csrf)_

HTML tersebut terpisah dengan `http://bank.com`, tetapi jika website tersebut tidak memiliki proteksi terhadap _CSRF attack_, maka HTML tersebut dapat mengeluarkan perintah ketika form disubmisi, pada kasus ini untuk mentransfer uang ke sang _hacker_.

Tentunya hal tersebut tidak diinginkan dalam website atau web app kita. Untuk mencegah hal ini, `CSRF token` digunakan. Token tersebut berguna untuk memastikan bahwa _request_ yang diberikan oleh _authenticated user_ benar-benar berasal dari user tersebut, bukan dari sembarang orang yang mengandalkan session user. Tentunya _hacker_ tidak memiliki akses terhadap token ini dan sulit untuk ditebak, kalau ada akses atau mudah ditebak maka konsep CSRF token ini sia-sia.

Mengutip dokumentasi Django [berikut](https://docs.djangoproject.com/en/4.1/ref/csrf/):

```
A CSRF cookie that is a random secret value, which other sites will not have access to.
```

Hal ini akan membuat website kita jauh lebih aman dari penyerangan ini, karena POST tersebut hanya akan jalan dari asal yang aman, seperti pada dokumentasi Django [berikut](https://docs.djangoproject.com/en/4.1/ref/csrf/):

```
This ensures that only forms that have originated from trusted domains can be used to POST data back.
```

### Membuat Elemen `<form>` Secara Manual

Hal ini dapat dilakukan dengan langkah sebagai berikut (mengambil contoh dari form `Login` project ini):<br/>

```html
<form method="POST" action="">
  {% csrf_token %}
  <label>Username:</label><br />
  <input type="text" name="username" required /><br />

  <label>Password:</label><br />
  <input type="password" name="password" required /><br />

  <input class="btn" type="submit" value="Login" />
</form>
```

1. Membuat form dengan method POST dan melibatkan CSRF Token<br/>
2. Membuat input dengan atribut `name` yang sesuai dengan yang diharapkan<br/>
3. Membuat input submit untuk submisi form<br/>

### Alur Submisi Data Melalui Form

1. User diperlihatkan halaman HTML yang berisi form submisi tertentu.<br/>

2. User mengisi form tersebut dengan nilai-nilai yang sesuai. Jika ada kesalahan dalam format atau tipe nilai yang dimasukkan, maka sebaiknya user diberitahu agar memperbaikinya.<br/>

3. User men-submit form tersebut.<br/>

4. Sebuah _request_ HTML akan terbentuk untuk menambah data tersebut ke database.<br/>

   Contoh handle _request_ tersebut:

   ```py
   if request.method == "POST":
       form = TaskForm(request.POST)
       if form.is_valid():
           new_task = form.save(commit=False)
           new_task.user = request.user
           new_task.save()
           return redirect("/todolist")
   ```

   Input user akan didapat di `form`. Jika input tersebut valid, maka akan di-save ke database.<br/>

5. Ketika mengakses halaman yang berisikan semua data pada database (misalnya semua data task seorang user), maka data tersebut akan terlihat pada halaman tersebut.

### Implementasi Checklist

1. Membuat aplikasi `todolist`<br/>
   Untuk membuat aplikasi baru yang bernama `todolist`, saya menjalankan perintah berikut:

   ```
   python manage.py startapp todolist
   ```

   Hal ini akan membuat suatu folder `todolist` yang dapat kita manfaatkan untuk membuat fitur todolist.

2. Menambahkan _path_ `todolist`<br/>
   Untuk mengimplementasikan hal tersebut, saya membuat file `urls.py` di folder `todolist`. Kemudian saya menambahkan kode berikut:

   ```py
   from django.urls import path

   app_name = "todolist"

   urlpatterns = []
   ```

   Kemudian saya memodifikasi file `project_django/urls.py` sebagai berikut:

   ```py
   urlpatterns = [
    ...,
    path('todolist/', include('todolist.urls')),
   ]
   ```

   Hal ini berarti semua _request_ user yang diawali dengan `/todolist` akan di-handle oleh `todolist/urls.py`
   .

3. Membuat model `Task`
   Untuk membuat hal tersebut, saya mengisi file `todolist/models.py` dengan kode berikut:

   ```py
   from django.db import models
   from django.contrib.auth import get_user_model

    # Create your models here.

    User = get_user_model()

    class Task(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        date = models.DateTimeField(auto_now_add=True)
        title = models.CharField(max_length=255)
        description = models.TextField()
        is_finished = models.BooleanField(default=False)
   ```

   Hal ini akan membuat model `Task` dengan atribut sesuai permintaan.<br/>
   a. Atribut `user` melibatkan argumen `on_delete=models.CASCADE` agar ketika user yang bersangkutan dihapus, maka object `task` yang dibuatnya juga terhapus.<br/>

   b. Atribut `date` melibatkan argumen `auto_now_add=True` agar ketika user membuat suatu object `task` baru, maka object tersebut memiliki _timestamp_ kapan object tersebut dibuat.<br/>

   c. Atribut `title` memiliki `max_length` 255 karena pertimbangan saya adalah seharusnya judul suatu task tidak perlu terlalu panjang.<br/>

   d. Atribut `description` adalah `TextField()`.<br/>

   e. Atribut `is_finished` adalah `BooleanField()`, dengan nilai _default_-nya `False`, karena tentunya saat task tersebut dibuat, asumsinya adalah task tersebut belum selesai dilakukan.

4. Membuat form register, login, dan logout user<br/>
   `Register`

   ```py
   # View untuk register
   def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun telah berhasil dibuat!")
            return redirect("todolist:login")

    context = {"form": form}
    return render(request, "todolist/register.html", context)
   ```

   Di sini, fungsi `register_user` akan membuat suatu `UserCreationForm`, di mana nanti form ini akan terlihat di halaman `register.html` sehingga kita tidak perlu secara manual membuat input untuk data yang ingin diambil dari user untuk register. Hal ini tentunya memudahkan kita untuk meng-handle kasus seperti ini.

   - Jika _method request_ user saat mengakses `/request` adalah `POST`, artinya user telah submit form yang diisinya untuk registrasi akun. Akan diperiksa apakah data yang user submit valid. Jika valid, maka akan di-save, yang berarti user akan terdaftar di database. User kemudian akan diarahkan untuk login, karena operasi tadi baru mendaftarkan akun.

   - Jika _method request_ user saat mengakses `/request` bukan `POST`, artinya user baru membuka halaman untuk mengisi data registrasi akun. Pada kasus ini, akan dikembalikan halaman `register.html` yang sudah diberikan `context` yang berisi form dari `UserCreationForm` di awal.

   ```html
   <!-- Template untuk register -->
   <section class="container">
     <h1>Registrasi Akun</h1>

     <form method="POST">
       {% csrf_token %} {% for field in form %}
       <div>
         {{ field.label_tag }}<br />
         {{ field }} {{ field.errors }}
       </div>
       {% endfor %}
       <input class="btn" type="submit" name="submit" value="Daftar" />
     </form>

     {% if messages %}
     <ul>
       {% for message in messages %} {{ message }} {% endfor %}
     </ul>
     {% endif %} Sudah mempunyai akun?
     <a href="{% url 'todolist:login' %}">Masuk</a>
   </section>

   {% endblock content %}
   ```

   Di sini, terdapat `<form>` yang sudah disisipkan `CSRF token`. Pada form tersebut akan di-render field-field terkait pembuatan user menggunakan `for-loop` yang diperoleh dari `context` yang di-pass di views `register_user` sebelumnya. Disajikan juga suatu input berupa submit yang akan mensubmisi data kepada server untuk diproses.

   Selain itu, disajikan pula pesan error, jika memang ada error, untuk memudahkan user ketika membuat suatu kesalahan saat memasukkan data.

   Sebagai tambahan, ada opsi bagi user yang sudah mendaftarkan akun untuk login dengan memencet tombol `Masuk`.

   `Login`

   ```py
   def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/todolist/")
        else:
            messages.info(request, "Username atau password salah!")

    return render(request, "todolist/login.html")
   ```

   Pada view ini, ada 2 kasus.

   - Jika saat mengakses `/login` _method request_ user adalah `POST`, artinya user ingin login ke akunnya. Maka akan dilakukan pengecekan apakah user dengan username dan password yang diinput ada di database. Jika ada, maka kita login user dengan `login()` yang dimiliki Django dan mengarahkan user ke home, yaitu `/todolist/`.
   - Jika saat mengakses `/login` _method request_ user bukan `POST`, artinya user baru ingin melihat halaman `login.html`. Maka kita akan render halaman tersebut ke user tanpa _passing_ `context` apapun ke HTML tersebut.

   ```html
   <section class="container">
     <h2>Login</h2>
     <form method="POST" action="">
       {% csrf_token %}
       <label>Username:</label><br />
       <input type="text" name="username" required /><br />

       <label>Password:</label><br />
       <input type="password" name="password" required /><br />

       <input class="btn" type="submit" value="Login" />
     </form>

     {% if messages %}
     <ul>
       {% for message in messages %}
       <p
         style="color: red; padding: 1rem 2rem; border: 1px solid; border-color: red;"
       >
         {{ message }}
       </p>
       {% endfor %}
     </ul>
     {% endif %} Belum mempunyai akun?
     <a href="{% url 'todolist:register' %}">Buat Akun</a>
   </section>
   ```

   Di sini dibuat form HTML secara manual. Atribut `name` pada kedua input krusial agar data dapat dikirimkan ke server untuk diproses. Input submit juga penting agar data dapat ter-submit. Akan disajikan juga pesan error jika ada kesalahan dalam input data.

   Selain itu, disediakan opsi bagi user untuk pindah ke halaman register jika belum membuat akun.

   `Logout`

   ```py
   def logout_user(request):
    logout(request)
    return redirect("todolist:login")
   ```

   View `logout_user` cukup sederhana, di mana di sini memanfaatkan fungsi `logout` yang dimiliki Django untuk logout user yang sedang login. Kemudian user akan diarahkan ke halaman login.

5. Membuat halaman utama `todolist`<br>
   Untuk membuat hal tersebut, saya membuat view ``home dan `home.html` sebagai berikut:

   ```py
   @login_required(login_url="/todolist/login/")
    def home(request):
        tasks = Task.objects.filter(user=request.user)

        context = {"tasks": tasks, "user": request.user}
        return render(request, "todolist/home.html", context)
   ```

   Fungsi tersebut hanya dapat dijalankan jika user sudah login. Jika belum, maka akan diarahkan ke halaman login. Fungsi tersebut akan mem-filter semua task yang dibuat oleh user (hal ini dapat dilakukan karena ada atribut `user` yang berupa ForeignKey yang tersambung dengan model `User`), dan mem-pass-nya ke `home.html` melalui `context`. Selain itu, saya juga menambahkan `user` sebagai variabel `context` untuk men-display username-nya di `home.html`.

   ```html
   <!-- Memasukkan username dan tombol logout -->
   <nav>
     <h1>To Do List</h1>
     <div class="nav-right">
       <strong>Halo, {{ user.username }}!</strong>
       <a class="btn" href="{% url 'todolist:logout' %}">Logout</a>
     </div>
   </nav>

   <div
     style="margin: 3rem 5rem 5rem 5rem; display: flex; flex-direction: column; justify-items: center; align-items: center;"
   >
     <table>
       <tr>
         <td class="table-header">Judul</td>
         <td class="table-header">Keterangan</td>
         <td class="table-header">Dibuat</td>
         <td class="table-header">Status</td>
         <!-- Termasuk membuat kolom Ubah Status dan Hapus untuk mengerjakan bonus -->
         <td class="table-header">Ubah Status</td>
         <td class="table-header">Hapus</td>
       </tr>

       <!-- Memasukkan data task -->
       {% for task in tasks %}
       <tr>
         <td>{{ task.title }}</td>
         <td class="description-col">{{ task.description }}</td>
         <td>
           {{ task.date | date:"N j, Y"}}<br />
           {{ task.date | date:"H:i"}}
         </td>
         <!-- Termasuk menggunakan atribut is_finished untuk men-display status task untuk mengerjakan bagian bonus -->
         <td>
           {% if task.is_finished %}
           <p class="tag completed" style="background-color: #22c55e">
             Selesai
           </p>
           {% else %}
           <p class="tag not-completed" style="background-color: #ef4444">
             Belum Selesai
           </p>
           {% endif %}
         </td>
         <!-- Termasuk menambahkan button untuk mengubah status task untuk mengerjakan bagian bonus -->
         <td>
           <a
             class="btn toggle-btn"
             href="{% url 'todolist:toggle_task' task.id %}"
           >
             Ubah
           </a>
         </td>
         <td>
           <a
             class="btn delete-btn"
             href="{% url 'todolist:delete_task' task.id %}"
           >
             Hapus Task
           </a>
         </td>
       </tr>
       {% endfor %}

       <tr>
         <td class="add-row" colspan="7">
           <a class="btn add-btn" href="{% url 'todolist:create_task' %}">
             Tambah Task
           </a>
         </td>
       </tr>
     </table>

     <!-- Menampilkan pesan error jika ada -->
     <div>
       {% if messages %} {% for message in messages %}
       <p
         style="color: red; padding: 1rem 2rem; border: 1px solid; border-color: red;"
       >
         {{ message }}
       </p>
       {% endfor %} {% endif %}
     </div>
   </div>
   ```

   Pada dasarnya, halaman ini memanfaatkan tag `<table>` untuk menyajikan semua task yang user miliki dalam format tabel. Hal yang disajikan adalah judul, deskripsi, waktu dibuat, status task, serta button untuk mengubah status task dan menghapus task. Halaman ini juga menampilkan pesan error jika terjadi suatu error.

6. Membuat halaman untuk menambah task<br/>
   Untuk membuat hal tersebut, saya membuat view untuk meng-handle _request_ tersebut dan `create_task.html` yang akan memuat form untuk membuat task baru.

   Di sini saya memanfaatkan model form sebagai berikut (file ini ada di `todolist/forms.py`):

   ```py
    from django.forms import ModelForm
    from todolist.models import Task

    class TaskForm(ModelForm):
        class Meta:
            model = Task
            fields = ["title", "description"]
   ```

   `TaskForm` akan dimanfaatkan di view berikut:

   ```py
   @login_required(login_url="/todolist/login/")
    def create_task(request):
        form = TaskForm()

        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect("/todolist")

        context = {"form": form}
        return render(request, "todolist/create_task.html", context)
   ```

   Konsepnya mirip dengan `register_user`, di mana jika _method request_ user saat mengakses `/create-task` adalah `POST`, artinya user ingin menambah task baru dan validasi input akan dilakukan. Jika valid, maka task akan ditambahkan ke database. Akhirnya, user akan diarahkan kembali ke halaman utama.

   Sementara itu, jika _method request_ user adalah bukan `POST`, artinya user baru tiba di `/create_task` dan `create_task.html` akan ditampilkan, diiringi dengan `context` yang berisi form untuk mengisi data task.

7. Membuat routing<br/>
   Agar fungsi-fungsi di atas dapat dimanfaatkan user, maka saya mengisi `urlpatterns` pada `todolist/urls.py` dengan `path()` berikut:

   ```py
   urlpatterns = [
        path("", views.home, name="home"),
        path("register/", views.register_user, name="register"),
        path("login/", views.login_user, name="login"),
        path("logout/", views.logout_user, name="logout"),
        path("create-task/", views.create_task, name="create_task"),
        path("toggle-task/<int:id>", views.toggle_task, name="toggle_task"),
        path("delete-task/<int:id>", views.delete_task, name="delete_task"),
    ]
   ```

   Untuk masing-masing `path`, maka akan dijalankan view yang bersangkutan.

8. Melakukan deployment ke Heroku<br/>
   Untuk mengimplementasikan hal tersebut, karena repository GitHub saya sudah terhubung dengan app Heroku (serupa dengan Tugas 3), maka saya perlu melakukan perintah berikut di terminal:<br/>

   ```
   git add .
   git status # hanya untuk memeriksa status file-file yang berubah
   git commit -m "<related-commit-message>"
   git push -u origin main
   ```

   Maka, perubahan baru di repository akan terlihat pula pada app Heroku.

9. Membuat dua akun pengguna dan tiga dummy data untuk masing-masing pengguna<br/>
   Untuk mengimplementasikan hal tersebut, saya melakukan hal berikut:<br/>
   a) Mengakses link [berikut](https://gibs-tugas-pbp.herokuapp.com/todolist), kemudian mengklik tombol `Daftar`.<br/>
   b) Mendaftarkan user pertama, yaitu dengan username Gib dan password hahasiuu.<br/>
   c) Mendaftarkan user kedua, yaitu dengan username pbpcool123 dan password hahasiuuu.<br/>
   d) Login dengan user pertama, kemudian mengklik tombol `Tambah Task`.<br/>
   e) Mengisi judul dan deskripsi task.<br/>
   f) Mengulangi penambahan task sampai ada 3 task untuk user Gib.<br/>
   g) Mengulangi langkah d-f dengan user kedua.<br/>

### Web Design

1. Macam-macam penyajian CSS kepada HTML<br>

   - `Inline CSS`<br>
     Inline CSS menyajikan _style_ kepada HTML dengan menambahkan atribut pada tag HTML yang bersangkutan.<br>
     Contoh:

   ```html
   <h1 style="color:red;">Hey!</h1>
   ```

   Kelebihan dari metode penyajian ini adalah kita tidak perlu memikirkan nama _class_ CSS untuk menghias atribut HTML yang terkait. Tetapi, dokumen HTML terkait mungkin menjadi cukup berantakan dengan _styling_, dan untuk pengubahan di kemudian hari tidak praktis.

   - `Internal CSS`<br>
     Internal CSS menyajikan _style_ kepada HTML dengan menambahkan _CSS selector_ yang terkait pada tag `<style>` di file HTML.<br>
     Contoh:

   ```html
   <style>
     h1 {
       color: red;
     }

     .btn {
       padding: 4px;
     }
   </style>

   <!-- Akan mendapatkan style dari <style> -->
   <h1>Hey!</h1>
   <p class="btn">Aku Tombol :)</p>
   ```

   Kelebihan dari metode ini adalah masalah yang dialami Inline CSS teratasi, di mana bagian HTML hanya terdiri dari tag HTML saja, sementara _style_-nya dipisah. Tetapi, file HTML yang terkait masih dapat menjadi terlal besar karena ada tag `<style>` tersebut. Selain itu, menentukan nama _class_ CSS cukup memakan waktu.

   `External CSS`<br>
   External CSS menyajikan _style_ kepada HTML dengan menambahkan _CSS selector_ yang terkait pada file CSS terpisah, dan file tersebut akan direferensi oleh file HTML terkait untuk memperoleh _style_.<br>
   Contoh:

   ```css
   h1 {
     color: red;
   }

   a {
     color: blue;
   }

   .container {
     margin: 2px 4px;
     padding: 4px;
     border: 1px solid;
   }
   ```

   Kelebihan dari metode ini adalah _separation of concern_ yang nyata antara HTML dan CSS. Untuk mengubah _style_ HTML terkait di kemudian hari juga lebih dimudahkan. Tetapi, seperti Internal CSS, pemberian nama _class_ CSS cukup memakan waktu.

2. Tag HTML<br>
   `<p>`<br>
   Tag ini dipakai untuk menampilkan teks.

   `<a>`<br>
   Tag ini digunakan untuk menampilkan _link_ kepada destinasi tertentu (_link_ eksternal, halaman lain dalam website, dan lain-lain).

   `<span>`<br>
   Tag ini dapat dipakai untuk menghias suatu teks tertentu dalam tag lain.<br>
   Contoh:

   ```html
   <p>Welcome to My <span style="...">Website</span></p>
   <p></p>
   ```

   `<strong>`<br>
   Tag ini digunakan untuk membuat _children_-nya memiliki _font-weight_ tebal.

   `<body>`<br>
   Tag ini menandai bagian _body_ HTML.

   `<style>`<br>
   Tag ini dapat menampung semua _style_ di halaman HTML terkait dengan memanfaatkan _CSS selector_.

   `<img>`<br>
   Tag ini digunakan untuk menampilkan foto di halaman HTML

   `<div>`<br>
   Tag ini digunakan untuk menjadi _container_ dari _children-children_-nya.

   `<nav>`<br>
   Tag ini digunakan untuk menandakan bagian navigasi (serupa dengan div, tetapi lebih deskriptif).

   `<section>`<br>
   Tag ini serupa dengan div, tetapi lebih deskriptif karena menggunakan istilah _section_.

   `<input>`<br>
   Tag ini digunakan untuk menampilkan box untuk user melakukan input.

   `button`<br>
   Tag ini digunakan untuk menampilkan tombol di halaman HTML.

3. Tipe CSS selector<br>
   `*`<br>
   Memilih semua elemen dalam halaman HTML.

   `.className`<br>
   Memilih semua elemen HTML yang memiliki nama _class_ `className`.

   `#id1`<br>
   Memilih elemen HTML yang memiliki ID _id1_.

   `h1, h2, a, input, atau elemen HTML lainnya`<br>
   Memilih elemen HTML yang terkait

   `:hover`<br>
   Mengendalikan perubahan yang akan terjadi jika suatu elemen di-_hover_ dengan _mouse_ user.

4. Implementasi checklist<br>
   a. Setup Tailwind

   Untuk tugas 5 ini, saya menggunakan Tailwind CSS untuk menghias halaman HTML. Untuk itu, saya mengikuti langkah di [_link_ berikut](https://tailwindcss.com/docs/installation/play-cdn) dan memodifikasi file `base.html`.

   b. Kustomisasi halaman `login`, `register`, dan `create-task`.

   `login`<br>
   Untuk itu, saya ingin menampilkan navbar sederhana di atas halaman, form di sebelah kiri halaman, dan animasi di sebelah kanan halaman. Saya menggunakan _class_ yang disediakan oleh Tailwind untuk mencapai desain yang saya inginkan.

   `register`<br>
   Halaman ini serupa dengan halaman `login`, hanya saja form registrasi akun saya letakkan di sebelah kanan halaman, dan elemen animasi di sebelah kiri halaman. Untuk menambah _class_ pada elemen form, saya menggunakan _package_ `django-widget-tweaks` yang memudahkan proses ini.

   `create-task`<br>
   Halaman ini mungkin yang paling sederhana, di mana hanya ada sebuah formulir untuk membuat _to-do_ baru. Saya memutuskan untuk meletakkan form tersebut di tengah halaman (setidaknya secara horizontal 😄). Untuk menambah _class_ pada elemen form, seperti pada halaman `register`, saya menggunakan _package_ `django-widget-tweaks` yang memudahkan proses ini.

   c. Kustomisasi halaman `todolist` menggunakan _cards_

   Untuk itu, saya ingin menampilkan suatu navbar yang memuat nama user dan tombol untuk _logout_ user di atas halaman. Kemudian, saya menyajikan _to-do_ user dengan div yang ujungnya dibulatkan sedikit agar memperoleh desain yang sederhana tetapi elegan. Di dalam _card_ tersebut ada judul, deskripsi, dan tanggal pembuatan _to-do_, serta tombol untuk mengubah status atau menghapus _to_do_.

   Jika user mengubah status menjadi selesai, maka border _card_ akan menjadi hijau, sedangkan jika belum diselesaikan, border akan tetap merah. Hal ini untuk memudahkan user membedakan task mana yang sudah atau belum selesai, disertai dengan penyajian yang sederhana.

   Jika user belum memiliki task, maka akan ditampilkan animasi dan keterangan bahwa ia belum mempunyai task. Hal ini bertujuan untuk membuat tampilan halaman lebih dinamis dan elegan.

   d. Membuat halaman responsif

   Untuk itu saya memanfaatkan fitur yang dimiliki Tailwind dalam meng-_handle_ _responsive design_. Namun, karena keterbatasan waktu, saya tidak sempat membuat navbar saya menjadi responsif.

   e. Implementasi bonus

   Untuk itu, saya memutuskan untuk membuat interaksi yang sederhana, yaitu menambahkan `hover:border-black` pada _container_ _card_, yang akan mengubah warna border _card_ menjadi warna hitam.
