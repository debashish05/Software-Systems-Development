from flask import jsonify
import requests
import json

# 1. signup login logout
# 2. Read menu from DB
# 3. Order food items
# 4. Generate bill (Logic and steps like previous part). Once the bill is
# generated,this transx is complete and incoming order requests will contribute
# to the next transx
# 5. View previous bill statements. Initially a list of transactions pertaining
# to that customer will be displayed. When the customer selects one of the
# transactions, the entire bill for that transaction will be displayed.
# 6. Adding new items to the menu along with its cost.


# You can have one static account for the chef. However, your backend service
# should be able to differentiate between a customer and a chef without the
# client explicitly specifying the same.


print("1) Chef Signup \n2) Customer Signup \n3) Chef SignIn")
print("4) Customer SignIn\n5) SignOut \n6) Display Menu \n7 Order Food")
print("8) Generate Bill \n9) View previous Bill statements ")
print("10) Add new item in Menu \n11) Quit")

# 7,8,9 left
role = 0  # 2 means chef, 1 means customer, 0 means no one


def client():
    """
        Client behaviour will start from here. Client can be customer as well
        as chef. Based on that functionality will be provided
    """
    choice = 0
    while True:

        response = ""
        choice = int(input("Enter choice: "))
        global role

        if choice == 1 or choice == 2:
            # singup for customer and chef
            if role != 0:
                response = "First logout, Then signup"
            else:
                role = 2
                if choice == 2:
                    role = 1

                userName = input("Enter User Name: ")
                password = input("Enter password: ")
                if role == 2:
                    data = {"userName": userName, "password": password,
                            "role": "chef"}
                else:
                    data = {"userName": userName,
                            "password": password, "role": "customer"}
                response = requests.post(
                    'http://localhost:8000/signup', json=data).content
                print(response.decode("utf-8"))
                response = ""

        elif choice == 3 or choice == 4:
            # login for customer and chef
            if role != 0:
                response = "First logout, Then login"
            else:

                role = 2
                if choice == 4:
                    role = 1

                userName = input("Enter User Name: ")
                password = input("Enter password: ")

                data = {"userName": userName, "password": password}
                response = requests.post(
                    'http://localhost:8000/login', json=data).content
                print(response.decode("utf-8"))
                response = ""

        elif choice == 5:
            # logout
            if role == 0:
                response = "First Loign then logout"
            else:
                role = 0
                response = requests.post(
                    'http://localhost:8000/logout').content
                print(response.decode("utf-8"))
                response = ""

        elif choice == 6:
            # display menu
            if role != 0:
                response = requests.get('http://localhost:8000/menu').content

                print("\n*********************Menu***************************")
                print("Item Name, Price of Half plate, Price of Full Plate")

                menuAsJson = json.loads(response)
                for i in menuAsJson:
                    print(menuAsJson[i]['itemName'], ",",
                          menuAsJson[i]['halfPrice'], ",",
                          menuAsJson[i]['fullPrice'])
                response = ""

            else:
                response = "First login to access this content"

        elif choice == 7:
            # order food

            if role != 0:

                x = list(map(str, input("Enter Order with space seperated"
                                        "entry. "
                                        'For placing order use, "item_name '
                                        'full/half '
                                        'quantity" & keep on entering as many '
                                        "enteries in this format you want to "
                                        "order & then finally hit"
                                        "enter. For eg. 1 half 2 1 full 4 and"
                                        "then hit  ENTER\n").split()))
                for i in range(0, len(x), 3):
                    itemName = x[i]
                    halfQty = 0
                    fullQty = 0
                    if(x[i+1].lower == "half"):
                        halfQty = int(x[i+2])
                    else:
                        fullQty = int(x[i+2])

                    data = {"itemName": itemName,
                            "halfQty": halfQty, "fullQty": fullQty}
                    response = requests.post(
                        'http://localhost:8000/takeOrder', json=data).content
                    response = ""

            else:
                response = "First login to access this content"

        elif choice == 8:

            # generate bill
            if role != 0:
                tip = input("Enter tip percent ")
                people = input("Enter no of people who will split the bill: ")
                lucky = input("lucky draw, 1: for yes, 0: for No ")

                response = requests.get(
                    'http://localhost:8000/generateBill').content
                """
                print("\n******************** Bill *************************")
                print("Item Name, Price of Half plate, Price of Full Plate")

                menuAsJson = json.loads(response)
                for i in menuAsJson:
                    print(menuAsJson[i]['itemName'],",",
                    menuAsJson[i]['halfPrice'],
                    ",",menuAsJson[i]['fullPrice'])
                response=""
                """
            else:
                response = "First login to access this content"

        elif choice == 10:
            if role != 2:
                response = "You are not a chef you can't add new item to menu"
            else:
                itemName = input("Enter Name of the item: ")
                halfPlate = input("Enter price of Half plate: ")
                fullPlate = input("Enter price of Full plate: ")

                data = {"itemName": itemName,
                        "halfPrice": halfPlate, "fullPrice": fullPlate}
                response = requests.post(
                    'http://localhost:8000/add_item', json=data).content

                response = response.decode("utf-8")

        elif choice == 11:
            break

        print(response)


if __name__ == '__main__':
    """
        Driver Code
    """
    client()

# post will create new entry. put will modify existing entry otherwise
# create new one
