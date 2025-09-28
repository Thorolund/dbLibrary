import sqlite3

def connect_db(path): #connecting db
    return sqlite3.connect(path)

def create_tables(db_connect=connect_db("dbL.db")): #creating tables (if not exist)
    curs = db_connect.cursor()
    
    curs.execute("""CREATE TABLE IF NOT EXISTS readers (
                    pr TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    age INTEGER NOT NULL)""")
    
    curs.execute("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    total INTEGER NOT NULL CHECK(total >= 1),
                    free INTEGER NOT NULL CHECK(free >= 0 and free <=total))""")
    
    curs.execute("""CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pr TEXT NOT NULL REFERENCES readers(pr),
                    book_id INTEGER NOT NULL REFERENCES books(id),
                    total INTEGER NOT NULL CHECK(total >= 1),
                    free INTEGER NOT NULL CHECK(free >= 0 and free <=total))""")
    
    curs.execute("""CREATE TABLE IF NOT EXISTS holds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pr TEXT NOT NULL REFERENCES readers(pr),
                    book_id INTEGER NOT NULL REFERENCES books(id),
                    total INTEGER NOT NULL CHECK(total >= 1),
                    free INTEGER NOT NULL CHECK(free >= 0 and free <=total))""")
    
    db_connect.commit()
    
    return 0

create_tables(connect_db("dbL.db"))
