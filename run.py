import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
from colorama import Fore, Style
from articles import Articles
from orders import Orders
from helpers import display_full_sheet


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
orders = SHEET.worksheet("orders")
inactive_articles = SHEET.worksheet("inactive_articles")


def back_to_main_menu():
    """Clear terminal and open main menu once user clicks enter"""
    options = ["Go back"]
    terminal_menu = TerminalMenu(
        options, title="Press enter to go back to the main menu"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Go back":
        os.system("clear")
        main_menu()


def lookup_article_end_menu():
    """
    Prints menu asking user to lookup another article or go back to
    the main menu.
    """
    options = ["Look up another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to look up another article?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Look up another article":
        os.system("clear")
        Articles.look_up_article(inventory)
        lookup_article_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def add_article_end_menu():
    """
    Asks user to either add another article or to go back to main menu
    """
    options = ["Add another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options,
        title="Do you want to add another article?",
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Add another article":
        os.system("clear")
        if Articles.build_article(inventory, inactive_articles):
            add_article_end_menu()
        else:
            edit_article_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def edit_article_end_menu():
    """
    Allows user to edit another article
    or to clear terminal and open main menu
    """
    options = ["Edit another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options,
        title="Do you want to edit another article?",
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Edit another article":
        os.system("clear")
        Articles.edit_article(inventory)
        edit_article_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def delete_article_end_menu():
    """
    Allows user to delete another/different article
    or to clear terminal and open main menu
    """
    options = ["Delete another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to delete another article?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Delete another article":
        os.system("clear")
        Articles.delete_article(inventory, inactive_articles)
        delete_article_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def register_order_end_menu():
    """
    Allows user to register another order
    or to clear terminal and open main menu
    """
    options = ["Register another order", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to register another order?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Register another order":
        os.system("clear")
        order_id = Orders.generate_order_id(orders)
        Orders.build_order(order_id, orders, inventory)
        register_order_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def display_orders_by_date_end_menu():
    """
    Allows user to display orders for another period
    or to clear terminal and open main menu
    """
    options = ["Search for different dates", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to search for different dates?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Search for different dates":
        os.system("clear")
        Orders.display_orders_by_date(orders)
        display_orders_by_date_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def lookup_order_end_menu():
    """
    Allows user to lookup another order
    or to clear terminal and open main menu
    """
    options = ["Search for different order", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to search for another order ID?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Search for different order":
        os.system("clear")
        Orders.lookup_order_by_id(orders)
        lookup_order_end_menu()
    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def sales_menu():
    """
    Displays the sales menu using simple terminal menu. Uses
    a switch statement to call different functions based on the user's choice.
    """
    print(
        Fore.LIGHTGREEN_EX
        + "SALES MENU"
        + Style.RESET_ALL
        + f"""
--------------------------------------------
Make your selection with the up and down arrows on your keyboard,
then press ENTER
"""
    )
    options = [
        "1. Display orders (by date)",
        "2. Look up order by ID",
        "3. Register an order",
        "4. Back to main menu",
    ]
    terminal_menu = TerminalMenu(options)
    menu_index = terminal_menu.show()
    match menu_index:
        case 0:
            os.system("clear")
            Orders.display_orders_by_date(orders)
            display_orders_by_date_end_menu()
        case 1:
            os.system("clear")
            Orders.lookup_order_by_id(orders)
            lookup_order_end_menu()
        case 2:
            os.system("clear")
            order_id = Orders.generate_order_id(orders)
            Orders.build_order(order_id, orders, inventory)
            register_order_end_menu()
        case 3:
            os.system("clear")
            main_menu()


def inventory_menu():
    """
    Displays the inventory menu using simple terminal menu. Uses
    a switch statement to call different functions based on the user's choice.
    """
    print(
        Fore.LIGHTGREEN_EX
        + "INVENTORY MENU"
        + Style.RESET_ALL
        + f"""
--------------------------------------------
Make your selection with the up and down arrows on your keyboard,
then press ENTER
"""
    )
    menu = [
        "1. Display inventory",
        "2. Look up article",
        "3. Add article",
        "4. Edit article",
        "5. Delete article",
        "6. Back to main menu",
    ]
    terminal_menu = TerminalMenu(menu)
    menu_index = terminal_menu.show()
    match menu_index:
        case 0:
            os.system("clear")
            print(
                Fore.LIGHTGREEN_EX
                + "INVENTORY - DISPLAYING FULL INVENTORY"
                + Style.RESET_ALL
                + f"""
--------------------------------------------
The below table contains the shop's full inventory."""
            )
            print(Fore.CYAN)
            display_full_sheet(inventory)
            print(Style.RESET_ALL)
            back_to_main_menu()
        case 1:
            os.system("clear")
            Articles.look_up_article(inventory)
            lookup_article_end_menu()
        case 2:
            os.system("clear")
            if Articles.build_article(inventory, inactive_articles):
                add_article_end_menu()
            else:
                edit_article_end_menu()
        case 3:
            os.system("clear")
            Articles.edit_article(inventory)
            edit_article_end_menu()
        case 4:
            os.system("clear")
            Articles.delete_article(inventory, inactive_articles)
            delete_article_end_menu()
        case 5:
            os.system("clear")
            main_menu()


def main_menu():
    """Displays the main menu using simple terminal menu"""
    print(
        Fore.LIGHTGREEN_EX
        + "MAIN MENU"
        + Style.RESET_ALL
        + f"""
--------------------------------------------
Make your selection with the up and down arrows on your keyboard,
then press ENTER
"""
    )
    menu = ["1. Inventory", "2. Sales", "3. Quit"]
    terminal_menu = TerminalMenu(menu)
    menu_index = terminal_menu.show()
    match menu_index:
        case 0:
            os.system("clear")
            inventory_menu()
        case 1:
            os.system("clear")
            sales_menu()
        case 2:
            os.system("clear")
            print(
                Fore.LIGHTGREEN_EX
                + "QUITTING PROGRAM"
                + Style.RESET_ALL
                + f"""
--------------------------------------------
Thank you for using SHOP REGISTER!

This program was created by Johanna Petersson, for educational purposes only.
"""
            )
            sys.exit()


def main():
    """Prints welcome message and calls main menu"""
    os.system("clear")
    print(
        Fore.LIGHTGREEN_EX
        + "WELCOME TO SHOP REGISTER!"
        + Style.RESET_ALL
        + f"""
--------------------------------------------
A simulation of a simple inventory and sales management program
for a toys shop.

The program allows it's users to display, add to, and edit, the
shop's inventory and order history data, hosted in a spreadsheet.
--------------------------------------------
"""
    )
    main_menu()


if __name__ == "__main__":
    main()
