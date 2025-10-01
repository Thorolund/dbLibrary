import sqlite3
import tech

def find_books(db_connect, title=None, author=None, genre=None):
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
