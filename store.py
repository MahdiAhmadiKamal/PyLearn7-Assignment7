import qrcode

PRODUCTS = []
CODES = []
GOODS = []
invoice = []

def purchase_invoice ():
    total_count = 0
    total_cost = 0
    f = open ("purchase_invoice.txt", "w")
    f.write (('< < < < < purchase invoice > > > > >')+ "\n\n")
    f.write (('code   name   price   count   total price\n'))
    for purchase in invoice:
        f.write ((purchase["code"]) + "   ")
        f.write ((purchase["name"]) + "   ")
        f.write ((purchase["price"]) + "   ")
        f.write (str(purchase["count"])+ "   ")
        f.write (str(purchase["total price"])+ "\n")
        total_count = total_count + purchase["count"]
        total_cost = total_cost + purchase["total price"]
    
    f.write('Total items in your shopping cart:'+"\n")
    f.write(str(total_count)+ "\n")
    f.write('The total cost of your purchase:'+"\n")
    f.write(str(total_cost)+ "\n")
    f.write('\n......thanks for your shopping......')
    f.close()


def read_from_database ():
    f = open ("database.txt", "r")
    
    for line in f:
        result = line.split (",")
        result[3] = result[3].strip()    # to remove \n from 4th element of the string
        dict = {"code": result[0], "name": result[1], "price": result[2], "count": result[3]}
        PRODUCTS.append (dict)
        CODES.append (dict['code'])
        GOODS.append (dict['name'])
        
    f.close ()

def write_to_database ():    # to transfer the information from PRODUCTS list to database           
    f = open ("database.txt", "w")
    for product in PRODUCTS:
        f.write ((product["code"]) + ",")
        f.write ((product["name"]) + ",")
        f.write ((product["price"]) + ",")
        f.write (product["count"]+ "\n")
    
    f.close ()

def show_menu ():
    print ("1- Add")
    print ("2- Edit")
    print ("3- QR Code")
    print ("4- Remove")
    print ("5- Search")
    print ("6- Show list")
    print ("7- Buy")
    print ("8- Exit")

def add ():
    code = input ("enter code: ")
    name = input ("enter name: ")
    price = input ("enter price: ")
    count = input ("enter count: ")
    new_product = {'code': code, 'name': name, 'price': price, 'count': count}
    PRODUCTS.append (new_product)

def edit ():
    code = input ("enter the product code: ")
    if code in CODES:
        for product in PRODUCTS:
            
            if product ['code'] == code:
                print (product)
                print ("name: 1")
                print ("price: 2")
                print ("count: 3")
                item = int (input("select the item you want to edit: "))
                while item != 1 and item != 2 and item != 3:
                    print ('select 1, 2, or 3')
                    item = int (input("select the item you want to edit: "))
                if item == 1:
                    product['name'] = input("enter the new name: ")
                    print ('Information updated successfully')
                elif item == 2:
                    product['price'] = input("enter the new price: ")
                    print ('Information updated successfully')
                elif item == 3:
                    product['count'] = input("enter the new count: ")
                    print ('<<<Information updated successfully>>>')
    else:
        print ('There is no product with this code in stock.')
        

def remove ():
    code = input ("enter the product code: ")
    for product in PRODUCTS:
        if product['code'] == code:
            print (product)
            PRODUCTS.remove(product)
            print ('The product has been successfully removed.')

def search ():
    user_input = input ('type your keyword: ')
    for product in PRODUCTS:
        if product['code'] == user_input or product['name'] == user_input:
            print (product["code"],"\t\t", product["name"],"\t\t", product["price"])
            break
    else:
        print ("not found")

def show_list ():
    print ("code\t\tname\t\tprice")
    for product in PRODUCTS:
        print (product["code"],"\t\t", product["name"],"\t\t", product["price"])


def buy ():
    cart = 0
    while True:
        code = input ("Enter 'f' to finish or enter the product code: ")
        if code == "f":
            total_count = 0
            total_cost = 0
            print ("\n< < < < < purchase invoice > > > > >")
            print ("\ncode   name   price   count   total price")
            
            for purchase in invoice:
                print ((purchase["code"]) , end="   ")
                print ((purchase["name"]) , end="   ")
                print ((purchase["price"]) , end="   ")
                print (str(purchase["count"]) , end="   ")
                print (str(purchase["total price"]))
                total_count = total_count + purchase["count"]
                total_cost = total_cost + purchase["total price"]
            print ('\nTotal items in your shopping cart:')
            print (str(total_count))
            print ('The total cost of your purchase:')
            print (str(total_cost),'\n')
            print ('...thanks for your shopping...\n')
            purchase_invoice ()
            break   

        elif code in CODES:
            n = CODES.index(code)
            name = GOODS[n]
            print ('The product:',name)
            asked = int(input('How many of this product do you want? '))
            for product in PRODUCTS:
                if product['code'] == code:
                    
                    availabe = int (product['count'])
                    if asked > availabe or availabe == 0:
                        print ("Sorry. There are not enough products in stock.")
                    elif asked <= availabe:
                        availabe = availabe - asked
                        cart = cart + asked
                        print ('your cart:',cart)
                        purchase = {"code": code, "name": name, "price": product['price'], "count": asked, "total price": int(product['price'])*asked}
                        invoice.append(purchase)
                        product['count'] = str (availabe)
                        write_to_database ()
                        break               
        else:
            print ('There is no product with this code in stock.')



def qr_code ():
    code = input ("enter the product code: ")
    for product in PRODUCTS:
        if product['code'] == code:
            print (product)
            img = qrcode.make (product)
            img.save (code + 'qr_code.png')
            print ('The QR code is successfully made.')
            


print ("Welcome to my store application.")
print ("Loading...")

read_from_database ()
print ("Data loaded.")

while True:
    show_menu ()
    choice = int (input ("enter your choice: "))
    
    if choice == 1:
        add ()
        write_to_database ()
    elif choice == 2:
        edit ()
        write_to_database ()
    elif choice == 3:
        qr_code ()
    elif choice == 4:
        remove ()
        write_to_database ()
    elif choice == 5:
        search ()
    elif choice == 6:
        show_list ()
    elif choice == 7:
        buy ()
        write_to_database ()
    elif choice == 8:
        write_to_database ()
        exit (0)
    else:
        print ("Enter a number between 1 and 8.")
