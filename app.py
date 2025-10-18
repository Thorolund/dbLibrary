import db
import repo
import service

def init_database():

    db_connect = db.connect_db("dbL.db")
    db.create_tables(db_connect)
    return db_connect


def demo_books(db_connect):
    repo.add_book(db_connect, "Булька Брабаулька", "Вова Солодков", "Гламур", 3)

    repo.add_book(db_connect, "Преступление и наказание", "Федор Достоевский", "Роман", 2)

    repo.add_book(db_connect, "1984", "Джордж Оруэлл", "Антиутопия", 1)

    repo.add_book(db_connect, "Мастер и Маргарита", "Михаил Булгаков", "Роман", 2)







def demo_readers(db_connect):

    pr1 = repo.add_reader(db_connect, "Иван Иванов", "89991112233", 25)
    pr2 = repo.add_reader(db_connect, "Петр Петров", "89994445566", 30)
    pr3 = repo.add_reader(db_connect, "Мария Сидорова", "89997778899", 22)
    
    return pr1, pr2, pr3



def demo_operations(db_connect, pr1, pr2, pr3):


    service.hold_book(db_connect, pr1, "Мастер и Маргарита", "Михаил Булгаков")
    service.hold_book(db_connect, pr2, "1984", "Джордж Оруэлл")
    service.hold_book(db_connect, pr3, "Булька Брабаулька", "Вова Солодков")
    

    service.take_book_home(db_connect, pr1, "Мастер и Маргарита", "Михаил Булгаков")
    service.take_book_home(db_connect, pr2, "Преступление и наказание", "Федор Достоевский")
    

    print(f"\nКниги, взятые читателем {pr1}:")

    borrowed = service.get_all_borrowed_by_reader(db_connect, pr1)

    for book in borrowed:

        print(f"  - {book[0]} ({book[1]}), выдана: {book[2]}")
    
    print(f"\nЗабронированные книги читателем {pr3}:")

    held = service.get_all_held_by_reader(db_connect, pr3)
    for book in held:
        print(f"  - {book[0]} ({book[1]}), забронирована: {book[2]}")
    
    # Возврат 
    service.return_book(db_connect, pr1, "Мастер и Маргарита", "Михаил Булгаков")






def search(db_connect):

    
    print("\nПоиск по жанру 'Роман':")
    results = service.search_books(db_connect, genre="Роман")
    for book in results:
        print(f"  - {book[0]} ({book[1]}), {book[2]}, всего: {book[3]}, свободно: {book[4]}")


    print("\nПоиск по автору 'Оруэлл':")
    results = service.search_books(db_connect, author="Оруэлл")
    for book in results:
        print(f"  - {book[0]} ({book[1]}), {book[2]}, всего: {book[3]}, свободно: {book[4]}")




def main():
    
    # Инициализация базы данных
    db_connect = init_database()
    
    # Демонстрация функционала
    demo_books(db_connect)
    pr1, pr2, pr3 = demo_readers(db_connect)
    demo_operations(db_connect, pr1, pr2, pr3)
    search(db_connect)
    
    # Автосброс бронирований (в демо-режиме обычно ничего не сбрасывает)
    print("\n=== АВТОСБРОС БРОНИРОВАНИЙ ===")
    service.auto_cancel_holds(db_connect)
    
    # Проверка просроченных книг
    print("\n=== ПРОВЕРКА ПРОСРОЧЕННЫХ КНИГ ===")
    overdue = service.get_overdue_books(db_connect)
    if overdue:
        for book in overdue:
            print(f"Просрочка: {book['full_name']} - '{book['title']}', должна была вернуть: {book['date_return']}")
    else:
        print("Просроченных книг нет")
    


main()