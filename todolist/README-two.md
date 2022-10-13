# Tugas 6 PBP

### _Asynchronous Programming vs Synchronous Programming_

Di dalam pemrograman sinkronus, setiap baris kode akan dijalankan secara _sequential_.

Misalkan ada kode berikut:

```js
const x = "hi";
console.log(x);
console.log(2 + 2);
```

Program akan berjalan dari baris pertama hingga ketiga. Artinya, baris kedua tidak akan berjalan sebelum baris pertama selesai dieksekusi. Hal tersebut berlaku di semua baris.

Di dalam pemrograman asinkronus, **konsep tunggu-menunggu ini ditiadakan**. Artinya, suatu baris n dapat berjalan meskipun baris (n-1) belum selesai dieksekusi. Artinya, user bisa melanjutkan kegiatannya di halaman HTML tanpa perlu menunggu suatu bagian program diselesaikan (seperti menunggu post Instagram berhasil _upload_, kita masih bisa melihat _timeline_ kita dan pindah ke bagian aplikasi lainnya).

### _Event-Driven Programming_

_Event-driven programming_ adalah suatu paradigma pemrograman yang menjadikan _event_ jantung dari program. Artinya, suatu fungsi atau bagian lain program tersebut akan berjalan jika terjadi suatu hal saat user menggunakan program (_event_), seperti klik tombol, _hover_ dengan mouse, atau _event_ lainnya. Hal ini berbeda dengan _procedural programming_, di mana interaksi antar-baris kode hanya internal, tidak dinamis dan tidak bisa dipengaruhi oleh pemicu-pemicu eksternal (kecuali input user, tetapi hal tersebut menurut saya berbeda dengan konsep _event_ pada kasus ini).

### AJAX _Asynchronous Programming_

Dengan AJAX, kita bisa melakukan pemrograman secara asinkronus. Pada dasarnya, dengan AJAX, kita bisa memperoleh data dari server sambil melakukan hal lain di halaman HTML. Ketika memperoleh kembalian data dari server hasil pengolahan _backend_ secara _asinkronus_, data tersebut dapat ditampilkan di halaman HTML, tanpa adanya _page reload_, sehingga halaman akan terasa lebih cepat dan interaktif.

### Implementasi Checklist

1. `AJAX GET`<br>
   Untuk mengimplementasikan hal tersebut, saya melakukan beberapa tahapan:

   - Membuat `view` baru<br>
     Di `todolist/views.py`, saya membuat fungsi yang akan mengembalikan seluruh _task_ user dalam format JSON.

     ```py
     @login_required(login_url="/todolist/login")
     def get_json_todolist(request):
        tasks = Task.objects.filter(user=request.user).order_by("is_finished")
        return HttpResponse(
            serializers.serialize("json", tasks), content_type="application/json"
        )
     ```

     `View` ini akan diakses dari _path_ `todolist/json` yang telah dikonfigurasi di `todolist/urls.py`.

     ```py
     urlpatterns = [
         ...
         path("json/", views.get_json_todolist, name="json"),
     ]
     ```

     Untuk mengambil task tersebut, di bagian `<script>` `todolist/templates/home.html`, saya menambahkan kode berikut:

     ```js
     const getTasks = () => {
       $.ajax({
         type: "GET",
         url: "{% url 'todolist:json' %}",
         dataType: "json",
         success: (tasks) => {
           if (tasks.length == 0) {
             const taskSection = document.querySelector(".tasks");
             taskSection.insertAdjacentHTML(
               "beforeend",
               `<div class="animation my-4 grid place-items-center">
                    <lottie-player src="https://assets9.lottiefiles.com/datafiles/vhvOcuUkH41HdrL/data.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop  autoplay></lottie-player>
                    <p>Waduh, kamu belum punya task.</p>
                </div>`
             );
           } else {
             tasks.map((task) => makeTaskCard(task));
           }
         },
         error: (err) => {
           console.log(err);
         },
       });
     };

     $(document).ready(() => {
       getTasks();
     });
     ```

     Bagian tersebut akan mengimplementasikan AJAX untuk mengambil seluruh data _task_. Data _tasks_ kembalian dari server akan diproses JavaScript agar membuat elemen _card_ di halaman HTML dengan `insertAdjacentHTML`.

2. `AJAX POST`

   Di `home.html`, saya membuat satu tombol berikut:

   ```html
   <button
     id="toggle-create-task-btn"
     class="px-4 py-2 bg-black text-white rounded-lg"
   >
     Tambah Task
   </button>
   ```

   Tombol ini akan menampilkan modal untuk menambahkan _task_ seperti berikut:

   ```html
   <div
     id="create-task-modal"
     class="hidden backdrop-brightness-50 backdrop-blur-sm w-screen h-screen fixed justify-center items-center top-0 left-0"
   >
     <div
       class="fixed bg-white p-10 rounded-xl container max-w-screen-sm max-h-screen"
     >
       <p class="text-xl font-bold mb-4">Buat Task Baru</p>
       <form id="create-task-form" class="w-full" method="POST" action="">
         {% csrf_token %}
         <label class="mb-4">Judul</label><br />
         <input
           class="w-full rounded-lg border-2 border-black mb-4"
           type="text"
           name="title"
           placeholder="Belajar SDA"
           required
         /><br />

         <label class="mb-4">Deskripsi</label><br />
         <textarea
           class="w-full rounded-lg border-2 border-black mb-4"
           name="description"
           placeholder="Binary Search Tree, Sorting"
           required
         ></textarea
         ><br />

         <input
           id="create-task-btn"
           class="cursor-pointer px-4 py-2 bg-black text-white w-full rounded-lg"
           type="submit"
           value="Tambah!"
         />
       </form>
     </div>
   </div>
   ```

   _Logic_ untuk menampilkan dan menutup modal ada di bagian `<script>`.

   ```js
   window.onload = () => {
     const modal = document.getElementById("create-task-modal");
     const toggleModalBtn = document.getElementById("toggle-create-task-btn");
     const toggleTaskBtn = document.getElementById("toggle-task-btn");
     const deleteTaskBtn = document.getElementById("delete-task-btn");
     const createTaskBtn = document.getElementById("create-task-btn");

     toggleModalBtn.onclick = () => {
       modal.style.display = "flex";
     };

     window.onclick = (e) => {
       if (e.target === modal) {
         modal.style.display = "none";
       }
     };
   };
   ```

   Untuk menambahkan _task_ secara asinkronus, dibuat _view_ berikut:

   ```py
   @login_required(login_url="/todolist/login/")
   def create_task_ajax(request):
    if (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and request.method == "POST"
    ):
        form = TaskForm(request.POST)
        if form.is_valid:
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            data = serializers.serialize(
                "json",
                [
                    new_task,
                ],
            )
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return HttpResponse(data, content_type="application/json")
    return HttpResponseBadRequest("An error occured.")
   ```

   Jika ada _request_ POST dari _client_ secara AJAX, maka data _task_ baru akan divalidasi dan disimpan di _database_. Kembalian dari _view_ ini adalah _task_ baru yang dapat dimanfaatkan JavaScript untuk langsung menampilkan _task_ baru di halaman.

   ```js
   createTaskBtn.onclick = (e) => {
     e.preventDefault();
     $.ajax({
       url: "{% url 'todolist:create_task_ajax' %}",
       type: "POST",
       dataType: "json",
       data: $("form#create-task-form").serialize(),
       success: (task) => {
         $("#create-task-form").trigger("reset");
         if ($(".animation").length) {
           $(".animation").remove();
         }
         makeTaskCard(task);
         modal.style.display = "none";
       },
       error: (err) => {
         console.log(err);
       },
     });
   };
   ```

   Akhirnya, modal akan ditutup (jika tidak ada error saat membuat _task_ baru).

   _View_ ini dapat diakses di _path_ `/todolist/add`, yang dikonfigurasi di sini:

   ```py
    urlpatterns = [
        ...
        path("add/", views.create_task_ajax, name="create_task_ajax"),
        ...
    ]
   ```

   _Path_ ini diakses di `<script>` bagian `createTsakBtn.onclick` di atas.

   Pada akhirnya, _task_ baru akan ditampilkan tanpa perlu dilakukan _page reload_.
