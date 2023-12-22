import os
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
from validators import Validators
from get_user_input import (
    get_quantity,
    get_price,
    get_article_number,
    get_article_name,
    confirm_user_entry,
)

data_validator = Validators()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("shop_register")

inventory = SHEET.worksheet("inventory")
# data = inventory.get_all_values()
# print(data)


def add_article():
    article = get_article_number()
    print("Article is ", article)
    article_name = get_article_name()
    price_in = get_price("in")
    user_confirm = False
    while not user_confirm:
        price_out = get_price("out")
        if price_out < price_in:
            print("Price out is lower than price in.")
            user_confirm = confirm_user_entry(price_out)
        else:
            user_confirm = True
    article_quantity = get_quantity()
    print(
        f"Article nr: {article}, Article name: {article_name}, Price in: {price_in}, Price out: {price_out}, Stock: {article_quantity}"
    )
    article_row = [article, article_name, price_in, price_out, article_quantity]
    inventory.append_row(article_row)


def main_menu():
    os.system("clear")
    print("Opening main menu")
    menu = ["1. Inventory", "2. Sales", "3. Quit"]
    terminal_menu = TerminalMenu(menu, title="Main menu")
    menu_index = terminal_menu.show()

    match menu_index:
        case 0:
            print("Opening inventory menu")
            inventory_menu()
        case 1:
            print("Opening sales menu")
        case 2:
            print("Quitting program")
            SystemExit


def inventory_menu():
    menu = [
        "1. Display inventory",
        "2. Look up article",
        "3. Add article",
        "4. Edit article",
        "5. Delete article",
        "6. Back to main menu",
    ]
    terminal_menu = TerminalMenu(menu, title="Inventory menu:")
    menu_index = terminal_menu.show()

    match menu_index:
        case 0:
            print("Displaying inventory")
        case 1:
            print("Looking up article")
        case 2:
            print("Adding article")
            add_article()
        case 3:
            print("Editing article")
        case 4:
            print("Deleting article")
        case 5:
            print("Back to main menu")
            main_menu()


def main():
    """
    Main function
    """
    print("Welcome to shop register!")
    main_menu()


main()

"""
quantity = get_quantity()
print(f"Quantity is: {quantity}")
print(f"Quantity is of type {type(quantity)}")

article_nr = get_article_number()
print(f"Artcile nr is {article_nr}")

name = get_article_name()
print(f"Article name is: {name}")

price_in = get_price("in")
print(f"Price is: {price_in}")

price_out = get_price("out")
print(f"Price out: {price_out}")
"""
