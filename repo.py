import sqlite3
import tech

def add_book(db_connect, title, author, genre, n):
    curs = db_connect.cursor()

    if tech.check_book_exist(db_connect, author, title):
        curs.execute("""UPDATE books
                        SET total = total + ?
                        WHERE author == ? AND title == ?""", (n, author, title))
    else:
        curs.execute("""INSERT INTO books (title, author, genre, total, free)
                        VALUES
                        (?, ?, ?, ?, ?)""", (title, author, genre, n, n))
        
    db_connect.commit()


def delete_book(db_connect, title, author, genre, n):     
    curs = db_connect.cursor()      
    check_not_holded = True          
    if check_not_holded:         
        curs.execute("""DELETE FROM books                          
                        WHERE author == ? AND title == ?""", (author, title))     

        db_connect.commit()             
        return True
    else:         
        return False
    
def add_reader(db_connect, full_name, phone, age=18):
    curs = db_connect.cursor()
    
    name = full_name.split()[0]
    surname = full_name.split()[1]
    
    pr = name[0]+surname[0] + str(len(name))+str(len(surname)) + phone[-4:]
    
    if not(tech.check_reader_exist(db_connect, pr)):

        curs.execute("""INSERT INTO readers (pr, full_name, phone, age)
                    VALUES
                    (?, ?, ?, ?)""", (pr, full_name, phone, age,))
        
        db_connect.commit()

        return True
    else:
        return False    

def delete_reader(db_connect, pr):
    curs = db_connect.cursor()
    
    curs.execute("""DELETE FROM readers
                    WHERE pr == ?""", (pr, ))
    
    db_connect.commit()
    
    return 0
