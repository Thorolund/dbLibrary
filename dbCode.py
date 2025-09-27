from sqlite3 import *

con = connect("db_L")
curs = con.cursor()

def create_tables(): #creating tables (if not exist)
    curs.execute("""CREATE TABLE IF NOT EXISTS readers (
                    pr TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    age INTEGER NOT NULL)""")
    
    con.commit()
    
    return 0

create_tables()