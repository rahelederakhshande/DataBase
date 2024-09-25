import configparser
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid

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
        student_schema = {
            "$jsonSchema":{
                "bsonType": "object",
                "required": ["student_id", "name", "age"],
                "properties":{
                    "student_id" : {
                        "bsonType": "string", 
                        "description": "must be string"
                    },
                    "name" : {
                        "bsonType": "string", 
                        "description": "must be string"
                    },
                    "age" : {
                        "bsonType": "integer", 
                        "description": "must be integer"
                    }

                }
            }
        }
        try:
            collection = self.db.create_collection(self.collection_name, 
                                            validator=student_schema)
        except:
            collection = self.db[self.collection_name]
        collection.create_index("student_id", unique=True)

class Student:
    def __init__(self, student_id, name, age, **attributes):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.attributes = attributes

    def change_to_dict(self):
        student = {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            **self.attributes
        }
        return student
class manage:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def add_student(self, student):
        student = student.change_to_dict()
        print(student)
        try:
            self.db_connection.db[self.db_connection.collection_name].insert_one(student)
            print("Added!")
        except Exception as e:
            print(e)

    def remove_student(self, student_id):
        result = self.db_connection.db[self.db_connection.collection_name].delete_one({"student_id":student_id})
        if result.deleted_count:
            print("Removed!")
        else:
            print("Not Found!")
    
    def search_one_student(self,student_id):
        data = self.db_connection.db[self.db_connection.collection_name].find({"student_id":student_id})
        data = list(data)
        if data: 
            for student in data:
                for key, value in student.items():
                    if key != "_id":
                        print(f"{key} ---> {value}")
                print(20*"_")
        else:
            print("This ID Not Exists!")

    def find_all_students(self):
        data = self.db_connection.db[self.db_connection.collection_name].find()
        data = list(data)
        for student in data:
            for key, value in student.items():
                if key != "_id":
                    print(f"{key} ---> {value}")
            print(20*"_")

    def update_student(self, student_id, updates):
        self.db_connection.db[self.db_connection.collection_name].update_one({"student_id":student_id}, {"$set":updates})



def main():
    db = MongoDBConnection()
    mg = manage(db)
    while True:
        print("\n1. Add Student\n2. Remove Student \n3. Search Studnet\n4. View All Students\n5. Update Student\n6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            student_id = input("Student ID: ")
            name = input ("Name: ")
            age = int(input("Age: "))
            attributes = {}
            while True:
                attr_name = input("new attr name or blank to exit: ")
                if not attr_name:
                    break
                attr_value = input("value: ")
                attributes[attr_name] = attr_value
            student = Student(student_id,name,age,**attributes)
            mg.add_student(student)
                
        elif choice == '2':
            student_id = input("Student ID: ")
            mg.remove_student(student_id)
            

        elif choice == '3':
            
            student_id = input("Student ID: ")
            mg.search_one_student(student_id)
    

        elif choice == '4':
            mg.find_all_students()

        elif choice == '5':
            student_id = input("Student ID: ")
            data =mg.db_connection.db[mg.db_connection.collection_name].find({"student_id":student_id})
            updates = {}
            data = list(data)
            for student in data:
                for key in student.keys():
                    if key != "_id" and key != "student_id":
                        new_value = input(f"Enter new value {key} or blank: ")
                        updates[key] = new_value
                    if updates:
                        mg.update_student(student_id,updates)

        elif choice == '6':
            break
    

if __name__ == "__main__":
    main()
        

