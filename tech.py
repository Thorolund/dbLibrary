import sqlite3
from datetime import*

def check_reader_exist(db_connect, pr:str) -> bool:
    """
    Checking Is Reader Exists
    """
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM readers
                    WHERE pr == ?""", (pr, ))
    
    return len([i for i in curs.fetchall()])>0

def check_book_exist(db_connect, title:str, author:str) -> bool:
    """
    Checking Is Book Exists
    """
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM books
                 WHERE title==? AND author==?""", (title, author))
    
    return len([i for i in curs.fetchall()])>0

def getdate():

    return datetime.now().strftime("%d/%m/%y")