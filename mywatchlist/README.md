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
   JSON adalah singkatan dari _JavaScript Object Notation_, di mana JSON menampung data-data aplikasi terkait dalam bentuk _key-value pair_.

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
   XML adalah singkatan dari _Extensible Markup Language_, di mana XML digunakan untuk melakukan _data-delivery_, seperti halnya JSON. Namun, hal yang membedakan antara XML dengan JSON adalah formatnya yang cukup serupa dengan HTML, di mana XML menggunakan _tags_ (contohnya `<firstname>Gibrano</firstname>`).

   Contoh dari XML adalah sebagai berikut:

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

text goes here

### Pemeriksaan _Routes_ dengan Postman

1. `mywatchlist/html`<br><br>
   ![mywatchlist/html](https://user-images.githubusercontent.com/70869295/191177256-4a9698d9-0579-41bf-b510-fc541f92fa43.png)

2. `mywatchlist/json`<br><br>
   ![mywatchlist/json](https://user-images.githubusercontent.com/70869295/191177273-f4fe2c95-ac57-4548-bbd0-01562d0c1d28.png)

3. `mywatchlist/xml`<br><br>
   ![mywatchlist/xml](https://user-images.githubusercontent.com/70869295/191177316-bfd46a9e-813e-4d16-8d07-fd3a4bdde1f7.png)
