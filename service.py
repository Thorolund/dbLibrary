import sqlite3

def book_book(connect, pr, title, author):
    curs = connect.cursor()

    checking_reader=True
    if checking_reader:

        curs.execute("""SELECT * FROM books 
                     WHERE title==? AND author==?""",(title, author))
        id_book=curs.fetchone()[0]
        curs.execute("""UPDATE books
                     SET free= free-1
                     WHERE id==?""", (id_book, ))
        curs.execute("""INSERT INTO holds """)
        
