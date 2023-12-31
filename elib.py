from faker import Faker
from datetime import datetime, timedelta
from itertools import accumulate
import pandas as pd
import numpy as np
import random
import os
import shutil

class ElibraryTables:

  def __init__(self):
    pass

  def category_table(self):

    """
    Fungsi untuk membuat tabel category

    Returns
    ---------
    category_table: data frame
      Data frame berisi kolom category_id dan category_name

    """

    category_id   = [1, 2, 3, 4, 5, 6]
    category_name = ['Thriller', 'Fantasy', 'Romance', 'History', 'Biography', 'Self-Help']

    category_table= pd.DataFrame(zip(category_id, category_name),
                                  columns = ['category_id', 'category_name'])
    return category_table

  def user_table(self):

    """
    Fungsi untuk membuat tabel user

    Returns
    ---------
    user_table: data frame
      Data frame berisi kolom user_id, first_name, last_name, email, password, city, dan registration_date

    """
    random.seed(42)
    Faker.seed(42)
    fake       = Faker('id_ID')
    numRec     = 1000

    user_id    = []
    name       = []
    email      = []
    password   = []
    city       = []
    registration_date   = []

    for _ in range(numRec):
      user_id.append(_+1)
      while True:
        f_name= fake.first_name()
        l_name= fake.last_name()
        names = f_name + ' ' + l_name
        passw = fake.password()
        mail  = f'{l_name.lower()}.{f_name.lower()}@xmail.com'
        if names not in name and passw not in password and mail not in email:
          name.append(names)
          email.append(mail)
          password.append(passw)
          break

      city.append(fake.city())

      start_date = datetime(2018, 1, 1)

      registration_date = accumulate(
          [start_date] + [timedelta(days = random.randint(0, 1)) for _ in range(numRec - 1)],
          lambda acc, _: acc + timedelta(days = random.randint(0, 1))
      )

    user_table = pd.DataFrame(zip(user_id, name, email, password, city,
                                  registration_date), columns = ['user_id', 'name', 'email', 'password', 'city', 'registration_date'])

    return user_table


  def library_table(self):

    """
    Fungsi untuk membuat tabel library

    Returns
    ---------
    library_table: data frame
      Data frame berisi kolom library_id, name, category_id, dan contact_person

    """
    library_id    = [1, 2, 3, 4, 5, 6]
    name          = ['Perspective', 'Imagination', 'Romansa', 'Nusantara', 'The People', 'Golden Star']
    category_id   = [1, 2, 3, 4, 5, 6]

    contact_person= ['Komaruddin', 'Haykal', 'Frans', 'Wayan', 'Ucok', 'Didi']

    library_table = pd.DataFrame(zip(library_id,
                                    name,
                                    category_id,
                                    contact_person), columns = ['library_id',
                                    'name',
                                    'category_id',
                                    'contact_person'])
    return library_table


  def book_table(self):

    """
    Fungsi untuk membuat tabel book

    Returns
    ---------
    book_table: data frame
      Data frame berisi kolom book_id, title, category_id, year, author, dan publisher
    """
    random.seed(42)
    Faker.seed(42)
    fake        = Faker()

    numRec      = 600

    book_id     = [ ]
    title       = [ ]
    category_id = [ ]
    year        = [ ]
    author      = [ ]
    publisher   = [ ]
    for _ in range(numRec):
      book_id.append(_+1)

      title_a, title_b, title_c, title_d, title_e, title_f = f'The Affair at {fake.city()}', f'The Hope of little {fake.name()}', f'The Beauty in {fake.city()}', \
                                                             f'The Fall of {fake.state()}', f'The life of {fake.name()}', f'I am not {fake.color_name()}'

      if title_a not in title:
        title.append(title_a)
      if title_b not in title:
        title.append(title_b)
      if title_c not in title:
        title.append(title_c)
      if title_d not in title:
        title.append(title_d)
      if title_e not in title:
        title.append(title_e)
      if title_f not in title:
        title.append(title_f)

      random_year = fake.random_int(min=1973, max=2020)
      year.append(random_year)

      author.append(fake.name())

      publisher.append(fake.city())

    category_id = [i % 6 + 1 for i in range(0, numRec+1)]

    book_table = pd.DataFrame(zip(book_id, title, category_id, year, author, publisher), columns =
                  ['book_id', 'title', 'category_id', 'year', 'author', 'publisher'])

    return book_table

  def loan_table(self):

    """
    Fungsi untuk membuat tabel loan, yaitu tabel yang berisi user yang sedang meminjam buku

    Returns
    ---------
    user_table: data frame
      Data frame berisi kolom loan_id, user_id, book_id, library_id, n_access, loan_date, due_date dan return_date

    """
    random.seed(42)
    Faker.seed(42)
    fake         = Faker()
    numRec       = 2150
                  #2150 diatur agar perulangannya menghasilkan output tanggal sampai akhir tahun 2023

    loan_id      = [i + 1 for i in range(numRec)]
    user_id      = [fake.random_int(min=1, max=705) for _ in range(numRec)]
    book_id      = [fake.random_int(min=1, max=600) for _ in range(numRec)]

    pattern_dict = {i: list(range(i, 601, 6)) for i in range(1, 7)}
    library_id   = [key for random_book_id in book_id for key, values in pattern_dict.items() if random_book_id in values]

    n_access     = [fake.random_int(1, 2) for _ in range(numRec)]

    start_date   = datetime(2020, 12, 1)
    loan_date_gen = accumulate(
          [start_date] + [timedelta(days=random.randint(0, 1)) for _ in range(numRec - 1)],
          lambda acc, _: acc + timedelta(days=random.randint(0, 1))
      )
    loan_date    = list(loan_date_gen)
    due_date     = [date + timedelta(days = 14) for date in loan_date]
    return_date  = [date + timedelta(days = random.randint(8, 14)) for date in loan_date]

    loan_table   = pd.DataFrame(zip(loan_id, user_id, book_id, library_id, n_access, loan_date, due_date, return_date),
                  columns = ['loan_id', 'user_id', 'book_id', 'library_id','n_access', 'loan_date', 'due_date', 'return_date'])

    return loan_table

  def generate_random_hold_date(self, loan_date):

    """
    Fungsi untuk menciptakan hold_date secara random

    Parameters
    ---------
    loan_date: timestamp
      Tanggal yang dijadikan acuan adalah loan_date untuk menghasilkan hold_date secara random

    Returns
    ---------
    loan_date + timedelta(days = days_difference): timestamp
      Penjumlahan antara date acuan dan jarak hari yang dimunculkan secara random

    """
    days_difference = random.randint(0, 1)
    return loan_date + timedelta(days = days_difference)

  def hold_table(self):

    """
    Fungsi untuk membuat tabel hold, yaitu tabel yang berisi user yang hendak meminjam buku, tetapi bukunya sedang dipinjam oleh user lain di tabel loan

    Returns
    ---------
    hold_table: data frame
      Data frame berisi kolom hold_id, user_id, book_id, library_id, n_access, dan hold_date

    """

    random.seed(42)
    Faker.seed(42)
    fake       = Faker()

    '''
    User_id yang ada di tabel hold adalah user_id 706 sampai 1000
    '''

    start_id   = 706
    end_id     = 1000
    numRec     = end_id - start_id

    hold_id    = [_+1 for _ in range(numRec)]
    user_id    = random.sample(range(start_id, end_id + 1), numRec)

    """
    Panggil book_table data frame, ambil secara random baris tertentu, khususnya pada kolom book_id dan library_id untuk hold_table. Munculkan n_access
    secara random, entah 1 atau 2.
    """
    book_df    = self.book_table()
    hold_book  = book_df.sample(n=numRec, random_state=42)
    book_id    = hold_book['book_id'].tolist()
    library_id = hold_book['category_id'].tolist()
    n_access   = [fake.random_int(1, 2) for _ in range(numRec)]

    """
    Panggil loan_table data frame, taruh di dalam variabel loan_date, gabungkan dengan hold_book table, hapus duplikat dari hasil merge, dan ambil kolom
    'loan_date' pada loan_table' sebagai 'hold_date' untuk hold_table. Asumsinya, user yang melakukan hold adalah user yang ingin meminjam buku, namun
    buku tersebut sedang dipinjam oleh user lain dan pinjaman oleh user lain tersebut tercatat di loan_date. Sehingga untuk menimbulkan crash antara
    kedua user yang loan dan hold, tanggal pinjaman keduanya harus dibentrokkan melalui generate_random_hold_date() secara random, entah itu 0 atau 1.
    """
    loan_data  = self.loan_table()
    date_check = pd.merge(hold_book, loan_data, on='book_id', how='left')
    date_check = date_check.drop_duplicates(subset='book_id', keep='last')
    date_check = pd.DataFrame({'loan_date': date_check['loan_date']})

    date_check['hold_date'] = date_check['loan_date'].apply(self.generate_random_hold_date)
    hold_date  = date_check['hold_date'].tolist()

    hold_table = pd.DataFrame(zip(user_id, book_id, library_id, n_access,
                              hold_date), columns = ['user_id', 'book_id',
                              'library_id', 'n_access', 'hold_date'])
    """
    Setelah data frame terbentuk, kolom 'hold_date' disortir agar tanggal yang lebih kemudian tidak mendahului. Lalu index diatur ulang. Setelah itu kolom
    'hold_id' dimasukkan ke dataframe dan ditempatkan di posisi paling awal (kiri). Selanjutnya baris yang memiliki NA dihapus. Baris yang memiliki value
    NA muncul karena baris tersebut memuat book_id yang tidak dipinjam oleh user. Dengan demikian, baris ini tidak diperlukan, karena hanya book_id yang
    sedang dipinjam oleh user X yang dapat 'nongol' di tabel hold untuk dipinjam oleh user Y.
    """
    hold_table = hold_table.sort_values('hold_date')
    hold_table = hold_table.reset_index(drop=True)
    hold_table.insert(0, 'hold_id', hold_id)
    hold_table = hold_table.dropna()

    return hold_table

  def generate_random_loan_date(self, loan_date):

    """
    Fungsi untuk menciptakan loan_date secara random

    Parameters
    ---------
    loan_date: timestamp
      Tanggal yang dijadikan acuan adalah loan_date untuk menghasilkan loan_date secara random

    Returns
    ---------
    new_date: timestamp
      Penjumlahan antara date acuan dan jarak hari yang dimunculkan secara random

    """
    days_difference = random.randint(1, 30)
    new_date = loan_date + timedelta(days = days_difference)
    return new_date


  def final_loan_table(self):

    """
    Fungsi untuk membuat tabel final_loan, yaitu gabungan tabel hold dan tabel loan. Mengapa digabung? Asumsinya adalah user yang hold kemudian dapat menjadi
    user yang loan, sehingga data mereka di hold mesti ada juga di loan.

    Returns
    ---------
    joined_loan_table: data frame
      Data frame berisi kolom loan_id, user_id, book_id, library_id, n_access, loan_date, due_date, return_date, dan returned_by

    """
    np.random.seed(42)
    Faker.seed(42)

    """

    Proses penggabungan ini terdiri dari 5 langkah. Empat langkah pertama adalah penggabungan dan langkah kelima adalah penambahan kolom baru.

    1
    hold_table
    Pertama-tama, dipanggil dulu hold_table, lalu kemudian dipilih secara random, mana yang akan masuk ke tabel loan. Mengapa dipilih secara random? Skenarionya,
    tidak semua user yang hold akan melakukan loan. Kemudian kolom 'hold_date' dihapus karena tidak dibutuhkan lagi.
    """

    hold_data     = self.hold_table()
    after_hold    = hold_data.drop(['hold_date'], axis = 1)
    num_deletions = np.random.randint(40, 50)
    rows_to_delete= np.random.choice(after_hold.index, size=num_deletions, replace=False)
    after_hold    = after_hold.drop(rows_to_delete)
    after_hold    = after_hold.reset_index(drop=True)

    """
    2
    loan_table
    Setelah hold_table terbentuk, panggil loan_table
    """

    loan_data     = self.loan_table()

    """
    3
    gabungkan hold & loan table
    Di bagian ini, hold & loan digabungkan hanya untuk mengambil kolom 'return_date' dari loan untuk dijadikan sebagai kolom 'loan_date' dari data hold. Asumsinya
    adalah user yang hold hanya dapat melakukan peminjaman setelah user yang loan mengembalikan buku (pada hari itu juga atau setelahnya). Untuk menyeleksi
    return_date apa yang dapat dijadikan sebagai loan_date, kita hapus terlebih dahulu rows yang memiliki duplikat dan simpan value yang tersimpan paling akhir.
    Setelah bagian yang penting sudah diambil, kita drop kolom yang tidak lagi diperlukan dan melakukan re-name pada kolom yang dibutuhkan.
    """

    hold_loan_data = pd.merge(after_hold, loan_data, on = 'book_id', how = 'left')
    hold_loan_data = hold_loan_data.drop_duplicates(subset = 'book_id', keep='last')
    hold_loan_data = hold_loan_data.drop(['hold_id', 'loan_id', 'user_id_y', 'library_id_y', 'n_access_y', 'loan_date', 'due_date'], axis = 1)
    hold_loan_data = hold_loan_data.rename(columns={'return_date':'loan_date', 'user_id_x': 'user_id', 'library_id_x': 'library_id', 'n_access_x':'n_access'})

    """
    Kolom loan_date yang sudah terbentuk di-generate kembali agar tanggalannya dapat persis seperti sebelumnya atau beberapa hari setelahnya. Tanggalan untuk kolom loan_date
    digenerate dengan memanggil fungsi generate_random_loan_date(). Setelah loan_date terbentuk, due_date dan return_date di-generate kembali dengan aturan due_date adalah 14 hari
    setelah loan_date dan return_date adalah 8 atau 14 hari setelah loan_date.
    """

    hold_loan_data['loan_date']   = hold_loan_data['loan_date'].apply(self.generate_random_loan_date)
    hold_loan_data['due_date']    = [date + timedelta(days=14) for date in hold_loan_data['loan_date']]
    hold_loan_data['return_date'] = [date + timedelta(days= random.randint(8,14)) for date in hold_loan_data['loan_date']]

    """
    4
    Semua kolom untuk hold user sudah terbentuk dan disimpan dalam data frame yang baru, yaitu hold_loan_data. Data frame ini kemudian digabungkan lagi dengan loan table yang
    ada pada fungsi loan_table yang sudah disimpan dalam variabel loan_data. Data gabungan kemudian disortir, untuk memastikan agar kolom loan_date dan due_date tersusun
    secara ascending. Setelah data disortir, barulah loan_id dimasukkan dan diletakkan pada posisi paling awal (kiri).
    """

    joined_loan_table = pd.concat([loan_data.drop(['loan_id'], axis = 1), hold_loan_data], ignore_index=True)
    joined_loan_table = joined_loan_table.sort_values(['loan_date', 'due_date'])
    joined_loan_table.insert(0, 'loan_id', [_ + 1 for _ in range(len(joined_loan_table))])

    """
    5
    menambahkan kolom returned_by pada tabel untuk mendeskripsikan mana pengembalian yang dilakukan oleh user sendiri dan mana pengembalian yang dilakukan oleh sistem. Asumsinya,
    pengembalian oleh sistem terjadi apabila user belum melakukan pengembalian ketika masa peminjamannya sudah masuk masa due_date.
    """

    joined_loan_table['returned_by'] = [random.choice(['user', 'system']) if row['due_date'] == row['return_date'] else 'user' for index, row in joined_loan_table.iterrows()]

    return joined_loan_table

    
  def create_dataframes(self):

    """
    Fungsi untuk membuat dan mengembalikan data frame untuk tabel 'category', 'user', 'library', 'book', 'hold', dan 'loan'.

    Returns
    -------
    data frame
        Sebuah data frame untuk tabel 'category', 'user', 'library', 'book', 'hold', dan 'loan'.
    """
    category_df = self.category_table()
    user_df = self.user_table()
    library_df = self.library_table()
    book_df = self.book_table()
    hold_df = self.hold_table()
    loan_df = self.final_loan_table()

    return category_df, user_df, library_df, book_df, hold_df, loan_df


  def export_dataframes_to_csv(self):

    """
    Fungsi untuk mengubah tabel category, user, library, book, hold, dan loan dari data frame ke csv dan menyimpannya ke folder lokal di komputer

    Returns
    ---------
        Menampilkan output dari fungsi print

    """

    #menempatkan lokasi folder yang mau dituju untuk file csv
    destination_folder = 'D:\e_lib dataset'

    #membuat folder, bila foldernya belum ada
    os.makedirs(destination_folder, exist_ok=True)

    #memanggil data frame dari method create_dataframes
    category_df, user_df, library_df, book_df, hold_df, loan_df = self.create_dataframes()

    #ekspor data frame ke csv
    category_df.to_csv(os.path.join(destination_folder, 'category_table.csv'), index=False)
    user_df.to_csv(os.path.join(destination_folder, 'user_table.csv'), index=False)
    library_df.to_csv(os.path.join(destination_folder, 'library_table.csv'), index=False)
    book_df.to_csv(os.path.join(destination_folder, 'book_table.csv'), index=False)
    hold_df.to_csv(os.path.join(destination_folder, 'hold_table.csv'), index=False)
    loan_df.to_csv(os.path.join(destination_folder, 'loan_table.csv'), index=False)

    print('Tabel sudah diekspor dalam bentuk csv. Silakan cek e_lib dataset folder!')

