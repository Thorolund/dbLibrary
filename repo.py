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
  
    curs.execute('''SELECT COUNT(*) FROM loans WHERE book_id IN 
                     (SELECT id FROM books WHERE title = ? AND author = ?)''', (title, author))
    loans_count = curs.fetchone()[0]
    
    curs.execute('''SELECT COUNT(*) FROM holds WHERE book_id IN 
                     (SELECT id FROM books WHERE title = ? AND author = ?)''', (title, author))
    holds_count = curs.fetchone()[0]


    
    if not(tech.check_book_exist(db_connect, title, author)):
        print(f"{author} - '{title}' isn't exist")
        return False
    
    if loans_count > 0 or holds_count > 0:
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
        return False

    curs.execute("""INSERT INTO readers (pr, full_name, phone, age)
                    VALUES
                    (?, ?, ?, ?)""", (pr, full_name, phone, age,))
        
    db_connect.commit()

    return True   


def delete_reader(db_connect, pr:str):
    """
    If Reader Exists And Not Loans/Holds - Delete Row From DataBase
    """
    curs = db_connect.cursor()

    curs.execute("SELECT COUNT(*) FROM loans WHERE pr = ?", (pr,))
    loans_count = curs.fetchone()[0]
    
    curs.execute("SELECT COUNT(*) FROM holds WHERE pr = ?", (pr,))
    holds_count = curs.fetchone()[0]
    
    if loans_count > 0 or holds_count > 0:
        print(f"Нельзя удалить читателя {pr}")
        return False
    if not tech.check_reader_exist(db_connect, pr):
        return False
    

    curs.execute("DELETE FROM readers WHERE pr = ?", (pr,))

    
    
    db_connect.commit()
    
    return True
