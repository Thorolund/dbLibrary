import sqlite3

def check_reader_exist(db_connect, pr):
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM readers
                    WHERE pr == ?""", (pr, ))
    
    return len([i for i in curs.fetchall()])>0

