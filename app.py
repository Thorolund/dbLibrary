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
add reader - 'ar'
delete reader - 'dr'
find book by filters - 'fb'
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
        elif mode == 'ar':
            full_name = input("Full name:   ")
            while (len(full_name.split()) != 2):
                print("Uncorrect name. Try again")
                full_name = input("Full name:   ")
            
            phone = input("Phone:   ")
            while (len(phone) < 4 or not(phone.isdigit())):
                print("Uncorrect phone. Try again")
                phone = input("Phone:   ")
            age = input("Age:   ")
            while (not(age.isdigit())):
                print("Uncorrect age. Try again")
                age = input("Age:   ")
            repo.add_reader(db_connect, full_name, phone, age)
        elif mode == 'dr':
            pr = input("Pr of reader:   ")
            repo.delete_reader(db_connect, pr)
        elif mode == 'fb':
            title = None
            author = None
            genre = None
            filters = input("Choose filters(Title Author Genre):    ")
            for filter in filters.split():
                if filter == "Title":
                    title = input("Title:   ")
                elif filter == "Author":
                    author = input("Author:   ")
                elif filter == "Genre":
                    genre = input("Genre:   ")
                else:
                    print(f"There isn't filter {filter}")
            result = service.find_books(db_connect, title, author, genre)
            for book in result:
                print(" ".join([str(i) for i in book]))
        
user_interface()