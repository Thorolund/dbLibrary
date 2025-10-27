import sqlite3
import tech

def add_book(db_connect:sqlite3.connect, title:str, author:str, genre:str, n:int = 1):
    """
    If Book Exists - Free+=n And Total+=n. If Not Exist - Create New Row In DataBase
    """
    curs = db_connect.cursor()

    if tech.check_book_exist(db_connect, title, author):
        curs.execute("""UPDATE books
                        SET total = total + ?, free = free + 1
                        WHERE author == ? AND title == ?""", (n, author, title))
    else:
        curs.execute("""INSERT INTO books (title, author, genre, total, free)
                        VALUES
                        (?, ?, ?, ?, ?)""", (title, author, genre, n, n))
    db_connect.commit()
    
    print("Book is added")
    return True


def delete_book(db_connect, title:str, author:str):
    """
    If Book Exists - Delete Row From DataBase
    """ 
    curs = db_connect.cursor()   

    book_id = tech.check_book_exist(db_connect, title, author, True)
    if not(book_id):
        print(f"{author} - '{title}' isn't exist")
        return False
    
    curs.execute("""SELECT loans.id, holds.id FROM books
                    LEFT JOIN loans ON loans.book_id == books.id
                    LEFT JOIN holds ON holds.book_id == books.id
                    WHERE books.id == ?""", (book_id, ))
    h_and_l = curs.fetchall()
    if h_and_l != [(None, None)]:
        print(f"Can't delete {author} - '{title}' 'cause it holded/loaned")
        return False
    
    curs.execute("DELETE FROM books WHERE title = ? AND author = ?", (title, author))  
   
    db_connect.commit()
    print(f"Book deleted")
    return True         

    
def add_reader(db_connect, full_name:str, phone:str, age:int=18):
    """
    If Primary Key Of Reader Not Exist - Create New Row In DataBase
    """
    curs = db_connect.cursor()
    
    name = full_name.split()[0]
    surname = full_name.split()[1]
    
    pr = name[0]+surname[0] + str(len(name))+str(len(surname)) + phone[-4:]
    
    if tech.check_reader_exist(db_connect, pr):
        print("Can't add reader. Analogy already added")
        return False

    curs.execute("""INSERT INTO readers (pr, full_name, phone, age)
                    VALUES
                    (?, ?, ?, ?)""", (pr, full_name, phone, age,))
        
    db_connect.commit()
    print("Reader is added")
    return True   


def delete_reader(db_connect, pr:str):
    """
    If Reader Exists And Not Loans/Holds - Delete Row From DataBase
    """
    curs = db_connect.cursor()
    
    if not tech.check_reader_exist(db_connect, pr):
        print(f"There isn't reader {pr}")
        return False

    curs.execute("""SELECT loans.id, holds.id FROM readers
                    LEFT JOIN loans ON loans.book_id == readers.pr
                    LEFT JOIN holds ON holds.book_id == readers.pr
                    WHERE readers.pr == ?""", (pr, ))
    h_and_l = curs.fetchall()
    if h_and_l != [(None, None)]:
        print(f"Can't delete reader {pr} 'cause it has holds/loans")
        return False
    
    curs.execute("DELETE FROM readers WHERE pr = ?", (pr,))
    print(f"Reader {pr} is deleted")
    db_connect.commit()
    return True
