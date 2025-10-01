import sqlite3

def check_reader_exist(db_connect, pr):
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM readers
                    WHERE pr == ?""", (pr, ))
    
    return len([i for i in curs.fetchall()])>0

def check_book_exist(db_connect, title, author):
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM books
                 WHERE title==? AND author==?""", (title, author))
    
    return len([i for i in curs.fetchall()])>0
