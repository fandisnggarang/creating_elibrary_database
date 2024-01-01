/*
__ DAFTAR ISI
-- A. QUERY UNTUK MEMBUAT TABEL
-- B. QUERY UNTUK MENGIMPOR DATASET
-- C. 5 QUERY UNTUK MENGUJI DATASET

*/

/********************************/
--A. QUERY UNTUK MEMBUAT TABEL
/********************************/

-- Membuat tabel category
CREATE TABLE public.category (
category_id INTEGER PRIMARY KEY,
category_name VARCHAR(100) NOT NULL UNIQUE
);

-- Membuat tabel library
CREATE TABLE public.library (
library_id INTEGER PRIMARY KEY, 
name VARCHAR(100) NOT NULL UNIQUE,
category_id INTEGER NOT NULL,
contact_person VARCHAR(100),
CONSTRAINT fk_category
	FOREIGN KEY(category_id)
	REFERENCES category(category_id)
	ON DELETE RESTRICT
);

-- Membuat tabel buku
CREATE TABLE public.book (
book_id INTEGER PRIMARY KEY, 
title VARCHAR(100) NOT NULL UNIQUE,
category_id INTEGER NOT NULL,
year INTEGER CHECK(year>=1000 and year<=9999),
author VARCHAR(100) NOT NULL,
publisher VARCHAR(100),
CONSTRAINT fk_category
	FOREIGN KEY(category_id)
	REFERENCES category(category_id)
	ON DELETE RESTRICT
);

-- Membuat tabel users
CREATE TABLE public.users (
user_id INTEGER PRIMARY KEY, 
name VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE, 
password VARCHAR(100) NOT NULL UNIQUE,
city VARCHAR(100),
registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Membuat tabel loan
CREATE TABLE public.loan (
loan_id INTEGER PRIMARY KEY, 
user_id INTEGER NOT NULL,
book_id INTEGER NOT NULL,
library_id INTEGER NOT NULL,
n_access INTEGER CHECK(n_access>0 and n_access<=2),
loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
return_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
returned_by VARCHAR(100) CHECK(returned_by IN('user', 'system')),
CONSTRAINT fk_users
	FOREIGN KEY(user_id)
	REFERENCES public.users(user_id)
	ON DELETE RESTRICT,
CONSTRAINT fk_book
	FOREIGN KEY(book_id)
	REFERENCES book(book_id)
	ON DELETE RESTRICT,
CONSTRAINT fk_library
	FOREIGN KEY(library_id)
	REFERENCES library(library_id)
	ON DELETE RESTRICT
);

-- Membuat tabel hold
CREATE TABLE public.hold (
hold_id INTEGER PRIMARY KEY, 
user_id INTEGER NOT NULL,
book_id INTEGER NOT NULL,
library_id INTEGER NOT NULL,
n_access INTEGER CHECK(n_access>0 and n_access<=2),
hold_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
CONSTRAINT fk_users
	FOREIGN KEY(user_id)
	REFERENCES public.users(user_id)
	ON DELETE RESTRICT,
CONSTRAINT fk_book
	FOREIGN KEY(book_id)
	REFERENCES book(book_id)
	ON DELETE RESTRICT,
CONSTRAINT fk_library
	FOREIGN KEY(library_id)
	REFERENCES library(library_id)
	ON DELETE RESTRICT
);

/********************************/
--B. QUERY UNTUK MENGIMPOR DATASET
/********************************/

-- Impor data tabel category
COPY
	category
FROM 'D:\e_lib dataset\category_table.csv'
DELIMITER ','
CSV
HEADER;

-- Impor data tabel library
COPY
	library
FROM 'D:\e_lib dataset\library_table.csv'
DELIMITER ','
CSV
HEADER;

-- Impor data tabel buku
COPY
	book
FROM 'D:\e_lib dataset\book_table.csv'
DELIMITER ','
CSV
HEADER;

-- Impor data tabel user
COPY
	users
FROM 'D:\e_lib dataset\user_table.csv'
DELIMITER ','
CSV
HEADER;

-- Impor data tabel loan
COPY
	loan
FROM 'D:\e_lib dataset\loan_table.csv'
DELIMITER ','
CSV
HEADER;

-- Impor data tabel hold
COPY
	hold
FROM 'D:\e_lib dataset\hold_table.csv'
DELIMITER ','
CSV
HEADER;

/********************************/
--C. 5 QUERY UNTUK MENGUJI DATASET
/********************************/

-- Pertanyaan 1
-- Mencari tahu user yang paling aktif meminjam buku.
SELECT 
	user_id, 
	name,
	city,
	COUNT (book_id) AS n_book
FROM loan
JOIN users USING(user_id)
GROUP BY 1, 2, 3
ORDER BY 4 DESC
LIMIT 10;

-- Pertanyaan 2
-- Mencari tahu karakteristik buku yang paling banyak dipinjam.
SELECT 
	book_id,
	title,
	year,
	category_name as category,
	COUNT(book_id) as number_of_book
FROM book
join category using(category_id)
join loan using(book_id)
GROUP BY 1, 4
ORDER BY 5 DESC
LIMIT 10;

-- Pertanyaan 3 
-- Mencari tahu bulan dengan jumlah pinjaman maksimal dan minimal.
WITH MonthlyLoanCounts AS (
    SELECT 
        EXTRACT(YEAR FROM loan_date) AS year,
        TO_CHAR(loan_date, 'Month') AS month,
        COUNT(*) AS loan_count
    FROM 
        loan
    GROUP BY 
        year, month
)
SELECT 
    year,
    month,
    loan_count
FROM (
    SELECT 
        year,
        month,
        loan_count,
        ROW_NUMBER() OVER (PARTITION BY year ORDER BY loan_count DESC) AS rank_desc,
        ROW_NUMBER() OVER (PARTITION BY year ORDER BY loan_count ASC) AS rank_asc
    FROM 
        MonthlyLoanCounts
) ranked
WHERE 
    rank_desc = 1 OR rank_asc = 1
ORDER BY 
    year, rank_desc, rank_asc;

-- Pertanyaan 4  
-- Mencari tahu perbandingan jumlah registered user vs user yang sudah pernah meminjam.
-- Mencari tahu perbandingan user yang melakukan antrian buku vs user yang setelah antri 
-- jadi meminjam buku tersebut.
WITH 
registered_user AS(
SELECT
	COUNT(*) AS registered_users
FROM 
	users
),
loan_user AS(
SELECT 
	COUNT(DISTINCT user_id) AS active_borrowers_count
FROM
	loan
),
hold_user AS (
SELECT
	COUNT(DISTINCT user_id) AS users_in_queue_count
FROM
	hold
),
holduser_to_loan AS (
SELECT
    COUNT(DISTINCT h.user_id) AS holdUser_inLoan
FROM
    hold h
JOIN
    loan l on h.user_id = l.user_id AND h.book_id = l.book_id
)
SELECT
	registered_users, 
	active_borrowers_count,
	users_in_queue_count,
	holdUser_inLoan
FROM registered_user, hold_user, loan_user, holduser_to_loan;

-- Pertanyaan 5
-- Mencari tahu berapa jumlah buku yang dikembalikan oleh user dan oleh sistem (per tahun)
WITH HoldLoanReturns AS (
    SELECT
        user_id,
        EXTRACT(YEAR FROM return_date) AS return_year,
        CASE
            WHEN returned_by = 'user' THEN 'by_user'
            WHEN returned_by = 'system' THEN 'by_system'
            ELSE 'other_return'
        END AS return_type
    FROM
        loan 
)
SELECT
    return_year,
    COUNT(CASE WHEN return_type = 'by_user' THEN 1 END) AS n_returned_by_user,
    COUNT(CASE WHEN return_type = 'by_system' THEN 1 END) AS n_returned_by_system
FROM
    HoldLoanReturns
GROUP BY
    1
ORDER BY
    1;