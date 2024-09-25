import configparser
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
# limit ====> code, title, price
class MongoDBConnection:
    @staticmethod
    def load_config(file_name="config.ini"):
        config = configparser.ConfigParser()
        config.read(file_name)
        return config
    
    def __init__(self, file_name="config.ini"):
        config = MongoDBConnection.load_config(file_name)
        mongo_host = config['mongodb']['host']
        mongo_port = int(config['mongodb']['port'])
        db_name = config['mongodb']['db_name']
        self.collection_name = config['mongodb']['col_name']
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client[db_name]
        self.setup_collection()

    def setup_collection(self):
        book_schema = {
            "$jsonSchema":{
                "bsonType": "object",
                "required": ["code", "title", "price"],
                "properties":{
                    "code" : {
                        "bsonType": "string", 
                        "description": "must be string"
                    },
                    "title" : {
                        "bsonType": "string", 
                        "description": "must be string"
                    },
                    "price" : {
                        "bsonType": "double", 
                        "description": "must be double"
                    }

                }
            }
        }
        try:
            collection = self.db.create_collection(self.collection_name, 
                                            validator=book_schema)
        except:
            collection = self.db[self.collection_name]
        collection.create_index("code", unique=True)
        

class Book:
    def __init__(self, code, title, price, **attributes):
        self.code = code
        self.title = title
        self.price = price
        self.attributes = attributes
        # {pages: 3000, year: 2020}

    def change_to_dict(self):
        book = {
            "code": self.code,
            "title": self.title,
            "price": self.price,
            **self.attributes
        }
        return book

class OnlineShop:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def add_book(self, book):
        book = book.change_to_dict()
        print(book)
        try:
            self.db_connection.db[self.db_connection.collection_name].insert_one(book)
            print("Added!")
        except Exception as e:
            print(e)

    def remove_book(self, code):
        result = self.db_connection.db[self.db_connection.collection_name].delete_one({"code":code})
        if result.deleted_count:
            print("Removed!")
        else:
            print("Not Found!")
        
    def find_all_books(self):
        data = self.db_connection.db[self.db_connection.collection_name].find()
        data = list(data)
        # shops = ["s1", "s2", ...]
        for book in data:
            for key, value in book.items():
                if key != "_id":
                    print(f"{key} ---> {value}")
            print(20*"_")

    def update_book(self, code, updates):
        self.db_connection.db[self.db_connection.collection_name].update_one({"code":code}, {"$set":updates})


def main():
    db = MongoDBConnection()
    shop = OnlineShop(db)
    while True:
        print("\n1. Add Book\n2. View All Books\n3. Update Book\n4. Remove Book\n5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            code = input("code: ")
            title = input("title: ")
            price = float(input("price: "))
            attributes = {}
            while True:
                attr_name = input("new attr name or blank to exit: ")
                if not attr_name:
                    break
                attr_value = input("value: ")
                attributes[attr_name] = attr_value
            book = Book(code, title, price, **attributes)
            shop.add_book(book)
            
        elif choice == '2':
            shop.find_all_books()

        elif choice == '3':
            # title, price
            code = input("code: ")
            # find_book_by_code
            updates = {}
            fields = ['title', 'price']
            for f in fields:
                new_value = input(f"Enter new value {f} or blank: ")
                if new_value:
                    if f == "price":
                        new_value = float(new_value)
                    updates[f] = new_value
            if updates:
                # {'title': "t5", 'price':47.3}
                shop.update_book(code, updates)

        elif choice == '4':
            code = input("code: ")
            shop.remove_book(code)

        elif choice == '5':
            break

if __name__ == "__main__":
    main()