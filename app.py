import db
import repo
import service

path = input("Input path:   ")
db_connect = db.connect_db(path)

def init_data_base():
    db.create_tables(db_connect)
    
def user_interface():
    mode = ""
    while (mode != 'q'):
        print("""Modes:
                quit - 'q'
                create tables - 'ctbls'""")
        mode = input()
        if mode == 'ctbls':
            init_data_base()
            
user_interface()