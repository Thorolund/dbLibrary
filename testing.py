import db
#import app
import tech
import service

print(tech.check_book_exist(db.connect_db("dbL.db"), "Обломов", "Гончаров"))