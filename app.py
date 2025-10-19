import db
import repo
import service

path = input("Input path:   ")
db_connect = db.connect_db(path)
    
def user_interface():
    mode = ""
    while (mode != 'q'):
        print("""======================
Modes:
quit - 'q'
create tables - 'ctbls'
add book - 'ab'
delete book - 'db'
======================""")
        mode = input()
        if mode == 'ctbls':
            db.create_tables(db_connect)
        elif mode == 'ab':
            title = input("Title:   ")
            author = input("Author:   ")
            genre = input("Genre:   ")
            n = input("Count:   ")
            if n.isdigit():
                repo.add_book(db_connect, title, author, genre, int(n))
            else:
                repo.add_book(db_connect, title, author, genre)
        elif mode == 'db':
            title = input("Title:   ")
            author = input("Author:   ")
            repo.delete_book(db_connect, title, author)
user_interface()