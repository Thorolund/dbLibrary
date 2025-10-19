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
        where_check += f" title == '{title}'"

    if author != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" author == '{author}'"
    
    if genre != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" genre == '{genre}'"
    
    if where_check != "":
            where_check = "WHERE" + where_check

    tsk = f"""SELECT title, author, genre, total, free FROM books {where_check}"""
    curs.execute(tsk)
    
    return [i for i in curs.fetchall()]

def booking_book(db_connect, pr:str, title:str, author:str):
    """
    Booking For Reader
    """

    curs = db_connect.cursor()
    
    if not tech.check_book_exist(db_connect, title, author):
        print(f"There isn't {author} - '{title}'")
        return False
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False

    curs.execute("""SELECT * FROM books 
                    WHERE title==? AND author==? AND free != 0""",(title, author))
    free_count = curs.fetchone()

    if not free_count:
        print(f"No free {author} - '{title}'")
        return False
    
    book_id = free_count[0]
    
    
    curs.execute("""SELECT COUNT(*) FROM holds 
                    WHERE pr = ?""", (pr,))
    active_holds = len([row for row in curs.fetchall()])

    if active_holds >= 5:
        print(f"Reader can't hold book 'cause holds too many books (>=5)")
        return False
    
    date=tech.getdate()

    curs.execute("""INSERT INTO holds (pr, book_id, date) 
                    VALUES (?, ?, ?)""", (pr, book_id, date))

    curs.execute("""UPDATE books
                     SET free= free-1
                     WHERE id==?""", (book_id, ))

    db_connect.commit()
    print(f"Reader {pr} holds {author} - '{title}'")
    return True



def cancel_booking(db_connect, pr, title, author):
    """
    Cancel Booking
    """
        
    curs = db_connect.cursor()
    
    if not tech.check_book_exist(db_connect, title, author):
        print(f"There isn't {author} - '{title}'")
        return False
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False
    
    curs.execute("""SELECT id FROM books
                    WHERE title==? AND author==?""", (title, author))
    book_id = curs.fetchone()[0]
    
    curs.execute("""SELECT id FROM holds 
                    WHERE pr == ? AND book_id == ?""", (pr, book_id))

    holds = curs.fetchone()
    if not holds:
        print(f"There isn't holds")
        return False
    
    hold_id = holds[0]
    curs.execute("""DELETE FROM holds 
                    WHERE id == ?""", (hold_id,))

    curs.execute("""UPDATE books
                    SET free= free+1
                    WHERE id==?""", (book_id, ))

    print(f"Booking a {author} - '{title}' for a {pr} remotely")
    db_connect.commit()
    return True

def take_book_home(db_connect, pr, title, author):
    """
    Reader Takes Book Home
    """
    
    curs = db_connect.cursor()
    
    if not tech.check_book_exist(db_connect, title, author):
        print(f"There isn't {author} - '{title}'")
        return False
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False
    
    curs.execute("""SELECT id FROM books 
                    WHERE title==? AND author==? """, (title, author))
    book_id = curs.fetchone()[0]

    curs.execute("""SELECT COUNT(*) FROM loans 
                    WHERE pr == ?""", (pr,))
    
    loans = len([row for row in curs.fetchall()])
    if loans >= 5:
        print(f"Reader can't hold book 'cause loans too many books (>=5)")
        return False
    

    curs.execute("""SELECT free FROM books 
                    WHERE id == ? AND free != 0""", (book_id,))
    free_count = curs.fetchone()

    
    curs.execute("""SELECT id FROM holds WHERE pr = ? AND book_id = ?""", (pr, book_id))
    has_hold = curs.fetchone()
    
    if not(free_count) and not(has_hold):
        print(f"Reader can't take book 'cause not free and not hold")
        return False
    

    if has_hold:
        curs.execute("""DELETE FROM holds WHERE pr == ? AND book_id == ?""", (pr, book_id))
    

    date=tech.getdate()
    curs.execute("""INSERT INTO loans (pr, book_id, date) 
                    VALUES (?, ?, ?)""", (pr, book_id, date))


    
    print(f"{author} - '{title}' is taken by reader {pr}")
    db_connect.commit()
    return True


def return_book(db_connect, pr, title, author):
    """
    Return Book
    """
    curs = db_connect.cursor()
    
    if not tech.check_book_exist(db_connect, title, author):
        print(f"There isn't {author} - '{title}'")
        return False
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False

    curs.execute("""SELECT id FROM books 
                 WHERE title==? AND author==? """,(title, author))
    
    book_id = curs.fetchone()[0]
    
    
    curs.execute("""SELECT * FROM loans 
                    WHERE pr == ? AND book_id == ?""", (pr, book_id))
    loan = curs.fetchone()
    if not loan:
        print(f"{author} - '{title}' wasn't taken by reader {pr}")
        return False
    loan_id = loan[0]
    curs.execute("""DELETE FROM loans 
                    WHERE id == ?""", (loan_id,))


    curs.execute("""UPDATE books
                     SET free= free+1
                     WHERE id==?""", (book_id, ))


    print(f"{author} - '{title}' is returned from reader {pr}")
    db_connect.commit()
    return True

def get_reader_loans(db_connect, pr):
    curs = db_connect.cursor()
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False
    
    curs.execute("""SELECT books.title, books.author, loans.date 
                    FROM loans 
                    JOIN books ON loans.book_id = books.id 
                    WHERE loans.pr = ?""", (pr,))
    alllines=curs.fetchall()
    final_loans=[]


    for i in  range(len(alllines)):
        date=alllines[i][2]
        date = datetime.strptime(date, "%d/%m/%Y")

        info_one=alllines[i].append((date+timedelta(days=14)).strftime('%d/%m/%Y'))

        final_loans=final_loans.append(info_one)
    
    return final_loans()



def get_reader_holds(db_connect, pr):
    curs = db_connect.cursor()
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False
    
    curs.execute('''SELECT books.title, books.author, holds.date 
                    FROM holds 
                    JOIN books ON holds.book_id = books.id 
                    WHERE holds.pr = ?''', (pr,))

    alllines=curs.fetchall()
    final_holds=[] 

    for i in  range(len(alllines)):

        date=alllines[i][2]
        date = datetime.strptime(date, "%d/%m/%Y")

        info_one = alllines[i].append((date+timedelta(days=5)).strftime('%d/%m/%Y'))

        final_holds = final_holds.append(info_one)
    
    return final_holds()

def get_prosrochka_books(db_connect):

    curs = db_connect.cursor()
    date = datetime.now()
    
    curs.execute('''SELECT readers.pr, readers.full_name, books.title, books.author, loans.date 
                    FROM loans 
                    JOIN readers ON loans.pr = readers.pr 
                    JOIN books  ON loans.book_id = books.id''')

    all_loans = curs.fetchall()
    prosrochka_books = []

    
    for loan in all_loans:

        loan_datetime = datetime.strptime(loan[4], "%d/%m/%y")
        return_date = loan_datetime + timedelta(days=14)
        
        
        if date > return_date:
            date_return = return_date.strftime("%d/%m/%y")
            loan[4] = date_return  
              
        prosrochka_books.append(loan)  
  
    return prosrochka_books

def auto_reset_holds(db_connect):
    """
    Reset All Holds That Expired
    """
    curs = db_connect.cursor()
    today = tech.getdate()
    
    curs.execute("""SELECT * FROM holds""")
    
    for row in curs.fetchall():
        date = row[3]
        if tech.date1_more_date2(date, today, 5):
            curs.execute("""DELETE FROM holds
                            WHERE id == ?""", (row[0],))
            curs.execute("""UPDATE books
                            SET free = free + 1
                            WHERE id == ?""", (row[2]))
    print("All expired loand reset")
    
        
