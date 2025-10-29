##This file will be used for functions related to item shops.

from colorama import Fore, Style, init

from NPC_classes import Shopkeeper

init(autoreset=True)

def shop_menu(shopkeeper): #Function for displaying a shop menu. 'shopkeeper' is replaced by whatever shopkeeper's shop you want to see.

    print(Fore.CYAN + f'\n{shopkeeper.name}: {shopkeeper.opening}')

    counter = 0 #Initiated to zero so that I can use it for numbering the shop items.
    valid_choices = []

    print(
        Fore.BLUE +
        "\n============================================\n" + Fore.BLUE +
        "========= " + Fore.YELLOW + f"Welcome to {shopkeeper.shopname}" + Fore.BLUE + " =========\n" + Fore.BLUE +
        "============================================\n"
        )
    for item, price, quantity in shopkeeper.shopitems: #This code looks in the 'shopitems' value in the shopkeeper class, which I initiated below.
        counter += 1 #Every time the code pulls (item, price, quantity), the counter adds 1.
        valid_choices.append(counter)
        print(
            Fore.BLUE + 
            "|" + Fore.YELLOW + ":" + Fore.BLUE + "|" + Fore.RESET + 
            f" {counter}) {item:<20} {price:>6}G {quantity:>4} " + 
            Fore.BLUE + "|" + Fore.YELLOW + ":" + Fore.BLUE + "|\n"
            ) #This is printed for every (item, price, quantity) found in shopkeeper.shopitems (which I defined below)
        
    counter += 1
    
    print(
        Fore.BLUE + 
            "|" + Fore.YELLOW + ":" + Fore.BLUE + "|" + Fore.RESET + 
            f" {counter}) {'Exit shop':<20} {' ':>6} {' ':>5} " + 
            Fore.BLUE + "|" + Fore.YELLOW + ":" + Fore.BLUE + "|\n"
        )
    print(
        Fore.BLUE + 
        "============================================\n"
        )
    
    return valid_choices
    
#The code between the [] are the item, price, and quantity. 
my_shopkeeper = Shopkeeper('Bob', 'Bob\'s Bobbles', [('Health Potion', 25, 9), ('Rusty Sword', 300, 1), ('Half-eaten sandwich', 2, 1)], 'The fuck you want, asshole?', 'Buy something already! ', 'That\'s not even an option, dumbass! ', 'Good riddance!')
#I initiated an instance 'my_shopkeeper' of the Shopkeeper class, with the .name value = 'Bob', .shopname = 'Bob's Bobbles', and .shopitems = [(),(),()]

#shop_menu(my_shopkeeper) #Runs the program with the shopkeeper I just created.


def shopping(shopkeeper):

    while True:
        valid_choices = shop_menu(shopkeeper)
        choice = ''
        while choice not in valid_choices:
            choice = int(input(f"{shopkeeper.choice}").strip())
            if choice not in valid_choices:
                print(f'{shopkeeper.error}')        
            elif choice in valid_choices:
                print('congrats')
                break

shopping(my_shopkeeper)
