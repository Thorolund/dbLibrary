import sqlite3

def add_book(db_connect, title, author, genre, n):
    curs = db_connect.cursor()
    
    curs.execute("""SELECT books
                 WHERE title==? AND author==?""", (title, author))
    if curs.fetchall():
        already_exists=True
    else:
        already_exists=False


    if already_exists:
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
        return "OK"     
    else:         
        return "No OK"
    
def add_reader(db_connect, full_name, phone, age=18): # db_connect, "Name Surname", 8**********, age
    curs = db_connect.cursor()
    
    name = full_name.split()[0]
    surname = full_name.split()[1]
    
    pr = name[0]+surname[0] + str(len(name))+str(len(surname)) + phone[-4:]




    curs.execute("""SELECT readers
                 WHERE pr==?""", (pr, ))
    
    if curs.fetchall():
        no_already_exists=True
    else:
        no_already_exists=False
    


    if no_already_exists:

        curs.execute("""INSERT INTO readers (pr, full_name, phone, age)
                    VALUES
                    (?, ?, ?, ?)""", (pr, full_name, phone, age,))
    else:
        return False    
    
    db_connect.commit()
    
    return 0

def delete_reader(db_connect, pr):
    curs = db_connect.cursor()
    
    curs.execute("""DELETE FROM readers
                    WHERE pr == ?""", (pr, ))
    
    db_connect.commit()
    
    return 0
