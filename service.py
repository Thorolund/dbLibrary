import sqlite3
import tech

def find_books(db_connect, title:str=None, author:str=None, genre:str=None):
    """
    Find Books By Many Filters
    """
    curs = db_connect.cursor()

    where_check = ""
    if title != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" title == {title}"

    if author != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" author == {author}"
    
    if genre != None:
        if where_check != "":
            where_check += " AND"
        where_check += f" genre == {genre}"
    
    if where_check != "":
            where_check = "WHERE" + where_check

    curs.execute(f"""SELECT * FROM books
                     {where_check}""")
    
    return [i for i in curs.fetchall]
def booking(db_connect,title,author):
    curs = db_connect.cursor()
    checking_reader=True
    if not(checking_reader):
        return False
    curs.execute("""SELECT * FROM books 
                     WHERE title==? AND author==?""",(title, author))
    id_book=curs.fetchone()[0]
    curs.execute("""UPDATE books
                     SET free= free-1
                     WHERE id==?""", (id_book, ))
    curs.execute("""INSERT INTO holds """)
    
    db_connect.commit()
    return True
