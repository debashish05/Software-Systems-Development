from enum import unique
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user
from flask_login import logout_user, login_required, UserMixin
from flask import jsonify
from flask import session
import csv
import sys
from random import randrange

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:password@localhost:3306/SSD"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stop printing warnings
app.config['SECRET_KEY'] = 'password'
app.config['SESSION_TYPE'] = "sqlachemy"

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db


class User(db.Model, UserMixin):
    """
            Will store the users and corresponding schema
    """
    userName = db.Column(db.String(30), primary_key=True, autoincrement=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    # comma seperated tids. Cant be unique because some user
    tid = db.Column(db.String(200))
    # may not give any order

    def __init__(self, userName, password, role, tids):
        self.userName = userName
        self.password = password
        self.role = role
        self.tid = tids


class Order(db.Model):
    """
            Store username and current id
    """
    userName = db.Column(db.String(30), primary_key=True, autoincrement=False)
    itemName = db.Column(db.String(50))
    fullQty = db.Column(db.Float)
    halfQty = db.Column(db.Float)

    def __init__(self, userName, itemName, halfQty, fullQty):
        self.userName = userName
        self.itemName = itemName
        self.fullQty = fullQty
        self.halfQty = halfQty


class Menu(db.Model):
    """ Will store the menu"""
    itemName = db.Column(db.String(50), primary_key=True, autoincrement=False)
    fullPrice = db.Column(db.Float)
    halfPrice = db.Column(db.Float)

    def __init__(self, itemName, halfPrice, fullPrice):
        self.itemName = itemName
        self.fullPrice = fullPrice
        self.halfPrice = halfPrice


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userName):
    return User.query.get(str(userName))


@app.route('/signup', methods=['POST'])
def signup():
    """Sign up Module"""
    data = request.get_json()
    check_user = User.query.filter_by(userName=data['userName']).first()

    if bool(check_user) is True:
        return "UserName already exists, Try different username"

    newCustomer = User(data['userName'], data['password'], data['role'], "")
    db.session.add(newCustomer)
    db.session.commit()
    return "Signup sucessfull and user added in the Database."


@app.route('/logout', methods=['POST'])
def logout():
    # session.pop('userName',None)
    session['logged_in'] = False
    return "Logged out from the site. Please revist again."


@app.route('/login', methods=['POST'])
def login():
    """ Login moudle"""
    data = request.get_json()
    user = User.query.filter_by(userName=data['userName']).first()
    if bool(user) is False:
        return "No user with this username exists"

    if(user.password != data['password']):
        return "Incorrect Password provided"

    session['logged_in'] = True
    session['userName'] = user.userName
    return "Login Successful"


@app.route('/menu')
def menu():
    """ Display menu"""
    menuOrder = {}
    items = Menu.query.all()
    for i in items:
        menuOrder[i.itemName] = {'itemName': i.itemName,
                                 'halfPrice': i.halfPrice,
                                 'fullPrice': i.fullPrice}
    menuOrder = jsonify(menuOrder)
    return menuOrder


@app.route('/take_order', methods=['POST'])
def takeOrder():
    """ take order from cutomer"""
    data = request.get_json()
    menu_Item = Order(userName=session['userName'], itemName=data['itemName'],
                      halfQty=data['halfQty'], fullQty=data['fullQty'])

    db.session.add(menu_Item)
    db.session.commit()

    return "New order Successfully added."


@app.route('/generateBill')
def generateBill():
    """ Generate bill"""
    pass
    menuOrder = {}
    items = Menu.query.all()
    for i in items:
        menuOrder[i.itemName] = {'itemName': i.itemName,
                                 'halfPrice': i.halfPrice,
                                 'fullPrice': i.fullPrice}
    menuOrder = jsonify(menuOrder)
    return menuOrder


@app.route('/add_item', methods=['POST'])
def add_item():

    data = request.get_json()
    check = Menu.query.filter_by(itemName=data['itemName']).first()

    if bool(check) is True:
        return "Item Id already exists."

    menu_Item = Menu(itemName=data['itemName'], halfPrice=data['halfPrice'],
                     fullPrice=data['fullPrice'])
    db.session.add(menu_Item)
    db.session.commit()
    return "New Item sucessfully added in the menu."


if __name__ == '__main__':
    db.create_all()
    app.run(port=8000, debug=True)


class Bill:
    """
            Will generate the bill
    """
    # item no:[half plate price, full plateprice], value is float key is string

    Menu = {}
    Order = {}  # value is float key is string
    Attribute = []  # List of attribute in menu, in strings
    tip = 0        # tip percent
    members = 0  # No of people who will split the bill
    total = 0
    discount = 0
    billSum = 0

    def readCSV(fileName):
        """
                Clear the old menu and populate the menu variable with
                new Menu based on the CSV file provided in parameter.
                First Line with be Attribute Name rest all are values
        """

        Menu.clear()                    # clear previous menu records
        file = open(fileName, 'r')
        csvreader = csv.reader(file)  # creating a csv reader object
        global Attribute
        # extracting field names through first row
        Attribute = next(csvreader)

        for line in csvreader:
            Menu[line[0]] = float(line[1]), float(line[2])

        file.close()

    def takeOrder():
        """
                Take order based on menu.Each line contain itme no. followed by
                quanity of half plate and full plate. Enter order with item no.
                quantity of half palate full plate. For the next item keep on
                continuing with space followed by order.Once order is finalized
                hit enter.
        """
        x = list(map(str, input("Enter Order with space seperated entry. "
                                'For placing order use, "item_name full/half '
                                'quantity" & keep on entering as many enteries'
                                "in this format you want to order & then "
                                "finally hit"
                                "enter. For eg. 1 half 2 1 full 4 and then hit"
                                " ENTER\n").split()))

        for index in range(0, len(x), 3):
            Order.setdefault(x[index], [0, 0])

            if x[index+1].lower() == "full":
                # order cant be fractional so int
                Order[x[index]][1] += int(x[index+2])
            elif x[index+1].lower() == "half":
                Order[x[index]][0] += int(x[index+2])

    def display(sheet):
        """
                Display menu or order based on Menu generated from csv file or
                order placed by the customer respectively. Print a dict
        """
        print()
        print(Attribute[0], Attribute[1], Attribute[2], sep=",")
        print()

        for key, value in sheet.items():
            print(key, value[0], value[1], sep=",")
            print()

    def totalAmount(Order, Menu):
        """ Display total amount"""

        sum = 0
        for key, value in Order.items():
            sum += Menu[key][0]*value[0]+Menu[key][1]*value[1]

        global total
        total = sum+sum*(tip/100)
        global billSum
        billSum = sum
        print("Total Bill (Including tip):", format(total, ".2f"), "\n")

    def luckyDraw():
        """
                Mechanism to play lucky draw base on no. generation from [0-99]
        """
        val = randrange(100)  # no less than 100 are generated

        if val < 5:  # range [0,4]
            discount = -0.5
        elif val >= 5 and val < 15:  # range [5,14]
            discount = -0.25
        elif val >= 15 and val < 30:  # range [15,29]
            discount = -0.10
        elif val >= 30 and val < 50:  # range [30,49]
            discount = 0
        else:  # range [50,99]
            discount = 0.20

        return discount

    def printDiscount():
        """
                Lucky Draw's output as per requirement
        """
        if discount < 0:  # recieved discount
            print("\nDiscount:", format((total)*discount, ".2f"))
            print("\n ****            ****")
            for i in range(3):
                print("|    |          |    |")

            print(" ****            ****\n")
            print("          {}")
            print("    ______________\n")

        else:
            print("\nIncrease:", format((total)*discount, ".2f"))
            print("\n **** ")
            for i in range(4):
                print("*    *")
            print(" **** \n")

    def finalBill():
        """
                Display the final bill and generate receipt
        """

        count = 0

        for key, value in Order.items():
            count += 1
            if value[0] != 0:
                print("Item ", key, " [Half] [", value[0], "]: ",
                      format(Menu[key][0]*value[0], ".2f"), sep="")

            if value[1] != 0:
                print("Item ", key, " [Full] [", value[1], "]: ",
                      format(Menu[key][1]*value[1], ".2f"), sep="")

        print("Total:", format(billSum, ".2f"))
        print("Tip Percentage: ", tip, "%", sep="")
        # print(discount)   #remove this
        print("Discount/Increase:", format((total)*discount, ".2f"))
        print("Final Total:", format((total)+(total)*discount, ".2f"))
        print("Update share of each member:", format(
            ((total)+(total)*discount)/members, ".2f"))

    def driver():
        """
                Driver Code
        """

        display(Menu)
        takeOrder()
        # display(Order)
        print()
        tip = int(input("Please select percentage of tip\n1. for 0% "
                        "\n2. for 10% \n3. for 20%:\n"))

        if tip == 1:
            tip = 0
        elif tip == 2:
            tip = 10
        else:
            tip = 20

        totalAmount(Order, Menu)

        members = int(input("Enter no of people who will split the bill: "))
        print("Each member need to pay:", format((total/members), ".2f"), "\n")

        contest = input('Do you want to Enter the contest "Test Your Luck".'
                        ' Type [yes/no]: ')

        if contest.lower() == "yes":
            discount = luckyDraw()
            printDiscount()

        finalBill()
