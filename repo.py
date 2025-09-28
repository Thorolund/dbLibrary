import sqlite3

def add_reader(connect, full_name, phone, age=18): # connect, "Name Surname", 8**********, age
    name = full_name.split()[0]
    surname = full_name.split()[1]
    
    curs = connect.cursor()
    
    pr = name[0]+surname[0] + str(len(name))+str(len(surname)) + phone[-4:]
    
    curs.execute("""INSERT INTO readers (pr, full_name, phone, age)
                    VALUES
                    (?, ?, ?, ?)""", (pr, full_name, phone, age,))
    
    connect.commit()
    
    return 0

