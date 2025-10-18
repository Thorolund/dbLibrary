import sqlite3
import tech
from datetime import*

def find_books(db_connect, title:str=None, author:str=None, genre:str=None):
    """
    Find Books By Many Filters
    """
    curs = db_connect.cursor()

    where_check = ""
    if title != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" title == {title}"

    if author != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" author == {author}"
    
    if genre != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" genre == {genre}"
    
    if where_check != "":
            where_check = "WHERE" + where_check

    curs.execute(f"""SELECT * FROM books
                     {where_check}""")
    
    return [i for i in curs.fetchall]




def getdate():

    return datetime.now().strftime("%d/%m/%y")



def booking_book(connection, pr, title, author):

    """
    booking for reader
    """

    curs = connection.cursor()
    

    curs.execute("SELECT * FROM books WHERE title==? AND author==? AND free!=0""",(title, author))
    free_count = curs.fetchone()
    book_id = curs.fetchone()[0]

    if not free_count:
        print(f"Нет свободных экземпляров книги '{title}'")
        return False
    
    
    curs.execute("SELECT COUNT(*) FROM holds WHERE pr = ?", (pr,))
    active_holds = curs.fetchone()[0]

    if active_holds >= 5:
        return False
    
    date=getdate()

    curs.execute("INSERT INTO holds (pr, book_id, date) VALUES (?, ?, ?)", (pr, book_id, date))

    curs.execute("""UPDATE books
                     SET free= free-1
                     WHERE id==?""", (book_id, ))


    return True



def cancel_booking(connection, pr, title, author):
    """Снятие бронирования книги"""
    curs = connection.cursor()
    curs.execute("SELECT id FROM books WHERE title==? AND author==? """,(title, author))
    book_id = curs.fetchone()[0]

    if not book_id:
        print(f"Книги '{title}' нет")
        return False

    
    curs.execute("SELECT id FROM holds WHERE pr = ? AND book_id = ?", (pr, book_id))

    if not curs.fetchone():
        return False
    
    curs.execute("DELETE FROM holds WHERE pr = ? AND book_id = ?", (pr, book_id))

    curs.execute("""UPDATE books
                     SET free= free+1
                     WHERE id==?""", (book_id, ))

    print(f"Бронирование книги '{title}' для читателя {pr} отменено")
    return True