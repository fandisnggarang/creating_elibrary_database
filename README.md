# Implementasi Database SQL untuk Aplikasi e-library
Dokumentasi singkat implementasi Database SQL

Ini adalah dokumentasi pembuatan database e-library yang menghimpun berbagai tabel. Secara garis besar, tabel-tabel tersebut memuat informasi mengenai siapa meminjam apa pada saat kapan. Hal-hal detail mengenai isi tabel akan dijelaskan pada bagian berikut. Adapun tujuan utama dari proses ini adalah sebagai bagian dari penuntasan rangkaian belajar materi ‘SQL’ di Pacmann. Sebagai rangkaian dari membangun database, siswa juga diminta untuk membangun dataset, yang memampukan siswa untuk mengaplikasikan kembali materi ‘python’ yang pernah dipelajari dengan aplikasi library pandas yang pernah diperoleh dalam materi ‘wrangling’.  Tools yang digunakan dalam proyek ini adalah pgAdmin 4, Google Colab, dan Visual Studio Code.

# Mission Statement

Aplikasi e-library yang dibuat terdiri atas 6 perpustakaan, yang menyimpan koleksi buku terbitan luar negeri dari bermacam-macam kategori. Dummy dataset pada aplikasi ini dibangun oleh python dengan menggunakan library Faker yang merekam data registrasi user pada tahun 2018-2019 dengan data pinjaman dari tahun 2020-2023. 

Database ini menggambarkan user orang Indonesia yang mengakses setiap perpustakaan dengan membuat akun terlebih dahulu. User meminjam buku apa saja, dalam hal ini ebook, yang tersedia berdasarkan kategori. Karena ini adalah ebook, maka kuantitas buku yang tersedia untuk dipinjam adalah 1. Hanya, untuk satu buku dapat diberikan maksimal 2 akses. Maka frasa “a diverse collection of books with varying quantities available for borrowing” yang tertulis pada soal tim Pacmann dimaknai sebagai jumlah buku sebanyak 1.

Dengan maksimal akses sebanyak dua untuk masing-masing user, artinya buku yang dipinjam user dapat diakses oleh maksimal satu orang lain selain peminjam. Ini dilakukan agar buku dapat dibaca oleh sebanyak mungkin orang. Karena menitikberatkan pada akses, maka kolom kuantitas buku ditiadakan dan diasumsikan telah terjawab dalam kolom akses. Buku yang dipinjam harus segera dikembalikan paling lama 14 hari setelah waktu pinjam. Jika tidak, akses terhadap buku secara otomatis ditutup oleh sistem. 

Apabila buku yang mau dipinjam sedang tidak tersedia, user menempatkan namanya pada daftar tunggu untuk mendapatkan maksimal dua akses. Ketika buku sudah tersedia, user memiliki waktu 7 hari untuk melakukan peminjaman. Bila lebih dari itu buku belum dipinjam oleh user, maka buku ditawarkan pada user lain yang ada di daftar tunggu berikutnya. 

Pembuatan database dan pembangunan dataset hanya terbatas pada kasus yang sudah bersifat historis. Adapun aspek input data pada aplikasi untuk user dan peminjaman baru di masa depan di luar kapasitas proyek ini. Limitasi lain pada proyek ini akan dijelaskan pada bagian terakhir dari dokumentasi ini sebagai rekomendasi untuk pengembangan lanjutan.


# Mendesain ERD
Aspek-aspek penting yang dibutuhkan untuk mendesain ERD adalah pembentukan struktur tabel dan aturan bisnis untuk tabel-tabel tersebut. 

## Struktur Tabel
Pertama, untuk pembentukan struktur tabel, ada 6 tabel yang diperlukan, yaitu tabel library, category, book, user, loan, dan hold. Keenam tabel tersebut dibangun di atas fitur-fitur, sebagaimana yang ditunjukkan dalam tabel di bawah ini. Secara umum, tabel library memuat nama perpustakaan, category mengenai genre, book tentang identitas buku, user berkaitan dengan identitas peminjam, loan menyimpan info mengenai pinjaman, dan hold berkaitan dengan data user yang berada dalam daftar antri pinjaman. 

<img width="1000" alt="gambar 1" src="https://github.com/fandisnggarang/generating_elibrary_dataset/assets/141505705/f37ad804-60b4-4fb8-b4a3-0c4b7e666845">

## Business Rules

Mulanya ditentukan tipe data, mana yang bertipe integer, varchar, dan timestamp. Setelah itu ditentukan aturan atau pembatas, seperti mana fitur yang wajib terisi, bersifat unik, atau lainnya. Terakhir adalah menentukan mana fitur yang berperan sebagai primary key dan mana yang bertindak sebagai foreign key. Untuk lebih jelas, silakan simak 6 butir aturan di bawah ini. 

1. Kolom name pada tabel library tidak boleh nol dan harus unik. Adapun category_id tidak boleh nol. 

2. Sama seperti kolom name, kolom category_name pada tabel category tidak boleh nol dan harus unik. 

3. Di book, yang unik adalah title. Category dan author tak boleh nol, year harus di antara 999-10000

4. Pada tabel users, yang harus unik adalah email & password. Name & registration_date tak boleh nol. 

5. Di loan, tanggal tak boleh nol, n_access harus berisi 1 atau 2. Returned_by harus berisi 'user'/'system'. 

6. Di tabel hold, yang tidak boleh nol adalah kolom hold_date dan n_access harus berisi nilai 1 atau 2

## Gambar ERD
Adapun relasi antar tabel dapat dilihat pada gambar ERD berikut. Sintaks pembuatan tabel dan dataset, serta impor dataset ke dalam tabel dapat disimak pada file-file terlampir. 

<img width="1000" alt="ERD pgerd" src="https://github.com/fandisnggarang/generating_elibrary_dataset/assets/141505705/bdc5e602-bad3-44e7-b53d-2b5c8da2aeca">

