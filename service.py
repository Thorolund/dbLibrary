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



def booking_book(db_connect, pr, title, author):

    """
    booking for reader
    """

    curs = db_connect.cursor()
    

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



def cancel_booking(db_connect, pr, title, author):
    """cancel booking"""
    curs = db_connect.cursor()
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




def take_book_home(db_connect, pr, title, author):
    """take book home"""
    curs = db_connect.cursor()
    
    curs.execute("SELECT id FROM books WHERE title==? AND author==? """,(title, author))
    book_id = curs.fetchone()[0]
    
    if not book_id:
        return False
    
    
    if not tech.check_reader_exist(db_connect, pr):
        return False
    

    curs.execute("SELECT COUNT(*) FROM loans WHERE pr = ?", (pr,))
    loans =curs.fetchone()[0]
    if loans >=5:
        return False
    

    curs.execute("SELECT free FROM books WHERE id = ? AND free !=0", (book_id,))
    free_count = curs.fetchone()

    
    curs.execute("SELECT id FROM holds WHERE pr = ? AND book_id = ?", (pr, book_id))
    has_hold = curs.fetchone()
    
    if not free_count and not has_hold:
        return False
    

    if has_hold:
        curs.execute("DELETE FROM holds WHERE pr = ? AND book_id = ?", (pr, book_id))

        curs.execute("""UPDATE books
                     SET free= free-1
                     WHERE id==?""", (book_id, ))
    

    date=getdate()
    curs.execute("INSERT INTO loans (pr, book_id, date) VALUES (?, ?, ?)", (pr, book_id, date))


    
    print(f"Книга '{title}' выдана читателю {pr}")
    return True


def return_book(connection, pr, title, author):
    """return book"""
    curs = connection.cursor()

    curs.execute("SELECT id FROM books WHERE title==? AND author==? """,(title, author))
    book_id = curs.fetchone()[0]


    if not book_id:
        return False
    
    
    curs.execute("SELECT * FROM loans WHERE pr = ? AND book_id = ?", (pr, book_id))
    if not curs.fetchone():
        return False
    
    curs.execute("DELETE FROM loans WHERE pr = ? AND book_id = ?", (pr, book_id))


    curs.execute("""UPDATE books
                     SET free= free+1
                     WHERE id==?""", (book_id, ))


    print(f"Книга '{title}' возвращена читателем {pr}")
    return True








def get_reader_loans(connection, pr):
    curs = connection.cursor()
    curs.execute('''SELECT books.title, books.author, loans.date 
        FROM loans 
        JOIN books ON loans.book_id = books.id 
        WHERE loans.pr = ?''', (pr,))
    alllines=curs.fetchall()
    final_loans=[]


    for i in  range(len(alllines)):
        data=alllines[i][2]
        info_one=alllines[i].append(data+timedelta(days=14).strftime('%d/%m/%Y'))
        final_loans=final_loans.append(info_one)
    
    return final_loans()



def get_reader_loans(connection, pr):
    curs = connection.cursor()
    curs.execute('''SELECT books.title, books.author, holds.date 
        FROM holds 
        JOIN books ON holds.book_id = books.id 
        WHERE holds.pr = ?''', (pr,))

    alllines=curs.fetchall()
    final_holds=[]


    for i in  range(len(alllines)):
        data=alllines[i][2]
        info_one=alllines[i].append(data+timedelta(days=5).strftime('%d/%m/%Y'))
        final_holds=final_holds.append(info_one)
    
    return final_holds()




