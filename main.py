from elib import ElibraryTables

tables_object  = ElibraryTables()

category_table = tables_object.category_table()
print(category_table)

user_table     = tables_object.user_table()
print(user_table)

library_table  = tables_object.library_table()
print(library_table)

book_table     = tables_object.book_table()
print(book_table)

hold_table     = tables_object.hold_table()
print(hold_table)

loan_table     = tables_object.final_loan_table()
print(loan_table)

all_dataframes = tables_object.create_dataframes()
print(all_dataframes)

tables_object.export_dataframes_to_csv()

