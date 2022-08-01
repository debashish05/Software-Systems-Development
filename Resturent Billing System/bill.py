import csv
from random import randrange


# item no: [half plate price, full plate price], value is float key is string
Menu = {}
Order = {}  # value is float key is string
Attribute = []  # List of attribute in menu, in strings
tip = 0		# tip percent
members = 0  # No of people who will split the bill
total = 0
discount = 0


def readCSV(fileName):
    """
            Clear the old menu and populate the menu variable with new Menu based on the
            CSV file provided in parameter. First Line with be Attribute Name rest all are values
    """

    Menu.clear()					# clear previous menu records
    file = open(fileName, 'r')
    csvreader = csv.reader(file)  # creating a csv reader object
    global Attribute
    Attribute = next(csvreader)		# extracting field names through first row

    for line in csvreader:
        Menu[line[0]] = float(line[1]), float(line[2])

    file.close()


def takeOrder():
    """
            Take order based on menu. Each line contain itme no. followed by quanity 
            of half plate and full plate. Enter order with item no. quantity of half palate
            full plate. For the next item keep on continuing with space followed by order.
            Once order is finalized hit enter. 

    """
    x = list(map(str, input("Enter Order with space seperated entry: ").split()))

    for index in range(0, len(x), 3):
        Order.setdefault(x[index], [0, 0])

        if x[index+1].lower() == "full":
            # order cant be fractional so int
            Order[x[index]][1] += int(x[index+2])
        elif x[index+1].lower() == "half":
            Order[x[index]][0] += int(x[index+2])


def display(sheet):
    """
            Display menu or order based on Menu generated from csv file or order placed by the 
            customer respectively. Print a dict
    """
    print()
    print(Attribute[0], Attribute[1], Attribute[2], sep=",")

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
    print("Total Bill (Including tip):", format(total, ".2f"), "\n")


def luckyDraw():
    """
            Mechanism to play lucky draw base on no. generation from [0-99]
    """
    val = randrange(100)  # no less than 100 are generated

    if val < 5:
        discount = -0.5
    elif val >= 5 and val < 15:
        discount = -0.25
    elif val >= 15 and val < 30:
        discount = -0.10
    elif val >= 20:
        discount = 0.20

    return discount


def printDiscount():
    """
            Lucky Draw's output as per requirement
    """

    if discount < 0:  # recieved discount
        print("The discount in the final price is:",
              int(abs(discount)*100), "%")

        print("\n ****      **** ")
        for i in range(3):
            print("|    |    |    |")
        print(" ****      ****\n")
        print("       {}  	")
        print("     ------    \n")
    else:
        print("The increase/no discount in the final price is: ",
              int(abs(discount*100)), "%", sep="")
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
        print("Item ", count, "[", value[0], " half, ", value[1], " full]: ",
              format(Menu[key][0]*value[0]+Menu[key][1]*value[1], ".2f"), sep="")

    print("Total:", format(total, ".2f"))
    print("Tip Percentage:", tip)
    # print(discount)	#remove this
    print("Discount/Increase:", format((total)*discount, ".2f"))
    print("Final Total:", format((total)+(total)*discount, ".2f"))
    print("Update share of each member:", format(
        ((total)+(total)*discount)/members, ".2f"))


if __name__ == '__main__':

    readCSV("Menu.csv")
    display(Menu)
    takeOrder()
    display(Order)
    tip = int(input("Enter tip Percent (Available choices 0%  10%  20%): "))
    totalAmount(Order, Menu)
    members = int(input("Enter no of people who will split the bill: "))
    print("Each member need to pay:", format((total/members), ".2f"))

    contest = input('Do you want to Enter into the contest "Test Your Luck".'
                    ' Type yes and hit enter or else press enter only: ')

    if contest.lower() == "yes":
        discount = luckyDraw()
        printDiscount()

    finalBill()
