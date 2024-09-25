from pymongo import MongoClient
from datetime import datetime
import json

# ------------Setup------------------
def read_data():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

config = read_data()
client = MongoClient(config["connection"])
db = client[config["db_name"]]
MenuItems = db[config["MenuItems_collection"]]
Orders = db[config["Orders_collection"]]
Customers = db[config["Customers_collection"]]
CustomerFeedback = db[config["CustomerFeedback_collection"]]
print("connected")

# ------------Menu Operations---------
def add_menu():
    menuname = input("Enter Menu Name: ")
    price = input("Enter Price: ")
    category = input ("Enter Category: ")
    ingredients = input ("Enter Ingredients: ")
    menu = MenuItems.find_one({"menuname" : menuname})
    if menu:
        print("MenuName already exists! Please Try Again")
        return
    menu = {
        "menuname" : menuname,
        "price": price,
        "category" : category,
        "ingredients" : ingredients
    }
    MenuItems.insert_one(menu)
    
    print("Menu Added!")

def view_menus():
    print("_"*10 + "Menus" + "_"*10)
    add_menus = MenuItems.find()
    for menu in add_menus:
        for k , v in menu.items():
            print(f"{k} ----> {v}")
        print()

def update_menu():
    menuname = input("Menu Name: ")
    new_name = input("New Menu Name: ")
    new_price = input("New Price: ")
    new_category = input("New Category: ")
    new_ingredients = input("New Ingredients: ")
    MenuItems.update_one({"menuname" : menuname},{"$set" : {"menuname" : new_name, "price" : new_price, "category" : new_category ,"ingredients": new_ingredients }})
    print("Menu Updated!")

def delete_menu():
    menuname = input("Menu Name: ")
    MenuItems.delete_one({"menuname" : menuname})
    print("Menu Removed!")

# ------------Customer Operations---------
def add_customer():
    customerid = input ("Enter ID: ")
    customername = input("Enter customer Name: ")
    phone = input("Enter Phone: ")
    address = input ("Enter Address: ")
    customer = Customers.find_one({"customerid" : customerid})
    if customer:
        print("Customer Already Exists!")
        return
    customer = {
        "customerid" : customerid,
        "customername" : customername,
        "phone" : phone,
        "address" : address
    }
    Customers.insert_one(customer)
    print("Customer Added!")

def view_customers():
    print("_"*10 + "Customers" + "_"*10)
    add_customer = Customers.find()
    for customer in add_customer:
        for k , v in customer.items():
            print(f"{k} ----> {v}")
        print()
    
def remove_customer():
    customerid = input("Customer ID: ")
    customer1 = Customers.find({"customerid" : customerid})
    if customer1:
        order_count = Orders.delete_many({"customerid" : customerid}).deleted_count
        print(f"Deleted {order_count} Orders")
        Customers.delete_one({"customerid" : customerid})
        print("Customer Removed!")
    else:
        print("Customer ID Not Found!")

# ------------Order Operations--------- 
def create_order():
    customerid = input("Customer ID: ")
    customer = Customers.find({"customerid" : customerid})
    if not customer:
        print("Customer Not Found!")
        return
    menuname = input("Menu Name: ")
    menu = MenuItems.find({"menuname" : menuname})
    if not menu:
        print("Menu Name Not Found!")
        return
    explain = input("Explain: ")
    order = {
        "customerid": customerid,
        "menuname": menuname,
        "explain": explain,
        "date": datetime.now()
    }
    Orders.insert_one(order)
    print("Order Added!")


def view_orders():
    print("_"*10 + "Orders" + "_"*10)
    all_orders = Orders.find()
    for order in all_orders:
        for k, v in order.items():
            print(f"{k} ----> {v}")
        print()

def update_order():
    customerid = input("Customer ID: ")
    customer = Customers.find({"customerid" : customerid})
    if not customer:
        print("Customer Not Found!")
        return
    menuname = input("Menu Name: ")
    new_menu = input("New Menu Name: ")
    new_explain = input("New Explain: ")
    Orders.update_one({"menuname" : menuname},{"$set" : {"menuname" : new_menu, "explain" : new_explain}})
    print("updated!")

def delete_order():
    customerid = input("Customer ID: ")
    Orders.delete_one({"customerid" : customerid})
    print("Order Removed!")

# ------------Feedback Operations--------- 
def add_feedback():
    customerid = input("CustomerID: ")
    customer = Customers.find_one({"customerid" : customerid})
    if not customer:
        print("Customer Not Found!")
        return
    else:

        menuname = input("Menu Name: ")
        feedback = input("FeedBack: ")
        C_feedback = {
            "customerid": customerid,
            "menuname": menuname,
            "feedback": feedback,
            "date": datetime.now()
        }
        CustomerFeedback.insert_one(C_feedback)
        print("FeedBack Added!")

def view_feedback():
    print("_"*10 + "FeedBack" + "_"*10)

    app_feedback = CustomerFeedback.find()
    for f in app_feedback:
        for k , v, in f.items():
            print(f"{k} ----> {v}")
        print()

# ------------Main----------------

def main_menu():
    while True:
        print("\nRestaurant Management System")
        print("1. Add Menu")
        print("2. View Menus")
        print("3. Update Menu")
        print("4. Delete Menu")
        print("5. Add Customers")
        print("6. View Customers")
        print("7. Remove Customers")
        print("8. Create Orders")
        print("9. View Orders")
        print("10. Update Orders")
        print("11. Remove orders")
        print("12. Add Feedback")
        print("13. View Feedback")
        print("14. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            add_menu()
        elif choice == '2':
            view_menus()
        elif choice == '3':
            update_menu()
        elif choice == '4':
            delete_menu()
        elif choice == '5':
            add_customer()
        elif choice == '6':
            view_customers()
        elif choice == '7':
            remove_customer()
        elif choice == '8':
            create_order()
        elif choice == '9':
            view_orders()
        elif choice == '10':
            update_order()
        elif choice == '11':
            delete_order()
        elif choice == '12':
            add_feedback()
        elif choice == '13':
            view_feedback()
        elif choice == '14':
            break
        else:
            print("Invalid! Please try again.")

if __name__ == "__main__":
    main_menu()