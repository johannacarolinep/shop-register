import os
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
from validators import Validators
from helpers import *
from get_user_input import *
from articles import Articles
from orders import Orders
from prettytable import PrettyTable

data_validator = Validators()
pretty_table = PrettyTable()

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


def build_article():
    """
    Asks user for an article number. If article already exists, asks user if
    they instead want to edit the article. If article number available,
    asks user for article name, price in, price out, and stock quantity.
    Adds the new article to the inventory sheet.
    """
    print(
        f"""ADD ARTICLES

Add a new article to the inventory.
--------------------------------------------
"""
    )
    article = get_article_number()
    if data_validator.validate_article_exists(article, inactive_articles):
        print(f"""Article with ID {article} already exists and is inactive.""")
    else:
        if data_validator.validate_article_exists(article, inventory):
            options = ["Yes", "No"]
            terminal_menu = TerminalMenu(
                options,
                title=f"""Article {article} already exists.
    Would you like to edit this article instead?""",
            )
            response = terminal_menu.show()

            if options[response] == "Yes":
                os.system("clear")
                Articles.edit_article(inventory, article)
                edit_article_end_menu()
            else:
                # Add another article or open main menu
                os.system("clear")
                add_article_end_menu()
        else:
            print("")
            print("Starting article creation")
            headers = inventory.row_values(1)
            temp_row = [[str(article), "-", "-", "-", "-"]]
            display_data(headers, temp_row)
            article_name = get_article_name()
            temp_row[0][1] = article_name
            display_data(headers, temp_row)
            price_in = get_price("in")
            temp_row[0][2] = price_in
            display_data(headers, temp_row)
            user_confirm = False
            while not user_confirm:
                price_out = get_price("out")
                if price_out < price_in:
                    print("Price out is lower than price in.")
                    user_confirm = confirm_user_entry(price_out)
                else:
                    user_confirm = True
            temp_row[0][3] = price_out
            display_data(headers, temp_row)
            article_quantity = get_quantity()
            temp_row[0][4] = article_quantity
            print("")
            print("Finished article:")
            display_data(headers, temp_row)
            article_instance = Articles(
                article, article_name, price_in, price_out, article_quantity
            )
            article_row = article_instance.to_row()
            add_row(article_row, inventory)


def delete_article():
    article = get_article_number()
    if data_validator.validate_article_exists(article, inventory):
        # display row
        print("Article to remove:")
        row_data = Articles.get_row_for_article(inventory, article)
        display_data(row_data[0], [row_data[1]])
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(
            options,
            title=f"Would you like to delete this article?",
        )
        response = terminal_menu.show()
        if options[response] == "Yes":
            add_row(row_data[1], inactive_articles)
            Articles.remove_row(article, inventory)
            print("Article removed")
        else:
            print("Cancelled")
    else:
        print("Article not found.")


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
    Asks user to aither add another article or to go back to main menu
    """
    options = ["Add another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options,
        title="Do you want to add another article?",
    )
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Add another article":
        os.system("clear")
        build_article()
        add_article_end_menu()

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
        delete_article()
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
        # register_order()
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
        f"""SALES MENU
--------------------------------------------
Make your selection with the up and down arrows on your keyboard,
then press ENTER
"""
    )
    options = [
        "Display orders (by date)",
        "Look up order by ID",
        "Register an order",
        "Back to main menu",
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
            # register_order()
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
        f"""INVENTORY MENU
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
            print("DISPLAYING INVENTORY")
            print("")
            display_full_sheet(inventory)
            back_to_main_menu()
        case 1:
            os.system("clear")
            Articles.look_up_article(inventory)
            lookup_article_end_menu()
        case 2:
            os.system("clear")
            build_article()
            add_article_end_menu()
        case 3:
            os.system("clear")
            Articles.edit_article(inventory)
            edit_article_end_menu()
        case 4:
            os.system("clear")
            delete_article()
            delete_article_end_menu()
        case 5:
            os.system("clear")
            main_menu()


def main_menu():
    """Displays the main menu using simple terminal menu"""
    print(
        f"""MAIN MENU
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
            print("Quitting program")
            SystemExit


def main():
    """Prints welcome message and calls main menu"""
    os.system("clear")
    print(
        f"""WELCOME TO SHOP REGISTER!
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
