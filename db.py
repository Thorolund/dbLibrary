import sqlite3

def create_tables(): #creating tables (if not exist)
    
    con = sqlite3.connect("db_L.db")
    curs = con.cursor()
    
    curs.execute("""CREATE TABLE IF NOT EXISTS readers (
                    pr TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    age INTEGER NOT NULL)""")
    
    curs.execute("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
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
    
    con.commit()
    
    return 0

def connect_db(path):
    return sqlite3.connect(path)

