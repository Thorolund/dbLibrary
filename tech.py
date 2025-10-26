import sqlite3
from datetime import*

def check_reader_exist(db_connect, pr:str) -> bool:
    """
    Checking Is Reader Exists
    """
    curs = db_connect.cursor()

    curs.execute("""SELECT * FROM readers
                    WHERE pr == ?""", (pr, ))
    
    return len([i for i in curs.fetchall()])>0

def check_book_exist(db_connect, title:str, author:str, return_id:bool=False):
    """
    Checking Is Book Exists
    """
    curs = db_connect.cursor()

    curs.execute("""SELECT id FROM books
                 WHERE title=? AND author=?""", (title, author))
    
    result = curs.fetchone()
    
    if return_id:
        return result[0] if result else False
    else:
        return bool(result)

def getdate():
    """
    Get Data %d/%m/%y
    """
    return datetime.now().strftime("%d/%m/%y")

def date1_more_date2(date1:str, date2:str, d_date:int) -> bool:
    """
    Date 1 + d_date > Date 2
    """
    date1 = datetime.strptime(date1, "%d/%m/%y") + timedelta(days=d_date)
    return date1 > (datetime.strptime(date2, "%d/%m/%y"))
    