import os
import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
from validators import Validators
from helpers import *
from get_user_input import (
    get_quantity,
    get_price,
    get_article_number,
    get_article_name,
    confirm_user_entry,
    get_sales_quantity,
    get_date,
    get_order_id,
)
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


def build_article():
    article = get_article_number()
    if data_validator.validate_article_existence(article, inventory):
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(
            options,
            title=f"Article {article} already exists. Would you like to edit this article?",
        )
        response = terminal_menu.show()

        if options[response] == "Yes":
            print("Opening edit function")
            edit_article(article)
        else:
            # Add another article or open main menu
            add_article_end_menu()
    else:
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
        article_instance = Articles(
            article, article_name, price_in, price_out, article_quantity
        )
        article_row = article_instance.to_row()
        add_row(article_row, inventory)
        # Add another article or open main menu
        add_article_end_menu()


def delete_article():
    article = get_article_number()
    if data_validator.validate_article_existence(article, inventory):
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
            Articles.remove_row(article, inventory)
            print("Article removed")
            # Delete different article or go back to main menu
            delete_article_end_menu()
        else:
            print("Cancelled")
            # Delete different article or go back to main menu
            delete_article_end_menu()
    else:
        print("Article not found.")
        # Delete different article or go back to main menu
        delete_article_end_menu()


def look_up_article():
    article_number = get_article_number()
    if data_validator.validate_article_existence(article_number, inventory):
        row_data = Articles.get_row_for_article(inventory, article_number)
        display_data(row_data[0], [row_data[1]])
    else:
        print("Article not found.")
    lookup_article_end_menu()


def edit_menu(article):
    options = ["Name", "Price_in", "Price_out", "Stock"]
    terminal_menu = TerminalMenu(
        options,
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        multi_select_empty_ok=True,
        title=f"Would you like to edit this article?",
    )
    response = terminal_menu.show()
    print("Response = ", response)
    if response is None:
        print("You did not make a selection. Re-routing to main menu.")
        # edit different article or back to main menu?
        main_menu()
    else:
        response_array = list(terminal_menu.chosen_menu_entries)
        print("Response array", response_array)
        row_index = Articles.get_row_index_for_article(article, inventory)

        if "Name" in response_array:
            print("Edit name:")
            new_name = get_article_name()
            column_index = 2
            inventory.update_cell(row_index, column_index, new_name)

        if "Price_in" in response_array:
            print("Edit price in:")
            new_price_in = get_price("in")
            column_index = 3
            inventory.update_cell(row_index, column_index, new_price_in)

        if "Price_out" in response_array:
            print("Edit price out:")
            current_price_in = inventory.cell(row_index, 3).value

            user_confirm = False
            while not user_confirm:
                new_price_out = get_price("out")
                if new_price_out < float(current_price_in):
                    print("Price out is lower than price in.")
                    user_confirm = confirm_user_entry(new_price_out)
                else:
                    user_confirm = True

            column_index = 4
            inventory.update_cell(row_index, column_index, new_price_out)

        if "Stock" in response_array:
            print("Edit stock:")
            new_stock = get_quantity()
            column_index = 5
            inventory.update_cell(row_index, column_index, new_stock)


def edit_article(article=None):
    if not article:
        article = get_article_number()

    if data_validator.validate_article_existence(article, inventory):
        # display row
        print("Article to edit:")
        row_data = Articles.get_row_for_article(inventory, article)
        display_data(row_data[0], [row_data[1]])
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(
            options,
            title="Would you like to edit this article?",
        )
        response = terminal_menu.show()
        if options[response] == "Yes":
            print("opening multi option menu")
            edit_menu(article)
            # Edit another article or back to menu
            edit_article_end_menu()
        else:
            # Edit another article or back to menu
            edit_article_end_menu()
    else:
        print("Article not found.")
        # Edit another article or back to menu
        edit_article_end_menu()


def back_to_main_menu():
    """
    Clear terminal and open main menu once user clicks enter
    """
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
    Allows user to lookup another article
    or to clear terminal and open main menu
    """
    options = ["Look up another article", "Back to main menu"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to look up another article?"
    )
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Look up another article":
        look_up_article()

    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def add_article_end_menu():
    """
    Asks user to aither add another article or to go back to main menu
    """
    options = ["Add another article", "Back to main menu"]
    terminal_menu = TerminalMenu(options, title="Do you want to add another article?")
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Add another article":
        build_article()

    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def edit_article_end_menu():
    """
    Allows user to edit another article
    or to clear terminal and open main menu
    """
    options = ["Edit another article", "Back to main menu"]
    terminal_menu = TerminalMenu(options, title="Do you want to edit another article?")
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Edit another article":
        edit_article()

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
        register_order()

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
        display_orders_by_date()

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
        lookup_order_by_id()

    elif options[confirm_response] == "Back to main menu":
        os.system("clear")
        main_menu()


def confirm_order_complete() -> bool:
    """
    Ask user if they want to add another row to sales order
    """
    options = ["Add row to sales order", "Order is complete"]
    terminal_menu = TerminalMenu(
        options, title="Do you want to add more articles to this order?"
    )
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Add row to sales order":
        return False

    elif options[confirm_response] == "Order is complete":
        return True


def confirm_order_final() -> bool:
    """
    Ask user if they want to finalize the sales order
    """
    options = ["Finalize order", "Cancel order"]
    terminal_menu = TerminalMenu(
        options,
        title="Select 'Finalize order' if you want to add this order to the system",
    )
    confirm_response = terminal_menu.show()

    if options[confirm_response] == "Finalize order":
        return True

    elif options[confirm_response] == "Cancel order":
        return False


def generate_order_id():
    current_id = orders.get_all_values()[-1][0]
    return int(current_id) + 1


def build_order(order_id):
    order = []
    order_complete = False
    while not order_complete:
        # ask for article id, verify exists
        article_number = get_article_number()
        if data_validator.validate_article_existence(article_number, inventory):
            # get sales quantity from user
            sales_quantity = get_sales_quantity(inventory, article_number, order)
            # calculate sum
            article_index = Articles.get_row_index_for_article(
                article_number, inventory
            )
            price_str = inventory.cell(article_index, 4).value
            price = float(price_str)
            sum = round(price * sales_quantity, 2)

            orders_instance = Orders(order_id, article_number, sales_quantity, sum)
            order_row = orders_instance.to_row()

            # add row to order
            order.append(order_row)

            # ask user if they want to add more rows
            order_complete = confirm_order_complete()

    # print order in table
    total_sum = 0
    for rows in order:
        total_sum += rows[4]

    total_sum = round(total_sum, 2)

    print("Order summary:")
    display_data(["Order ID", "Date", "Article", "Quantity", "Sum"], order)
    print(f"Total order sum: {total_sum}")

    # Add order to sheet if user confirms
    if confirm_order_final():
        for rows in order:
            add_row(rows, orders)
            # decrement inventory stock level by sold quantity
            article_id = rows[2]
            article_index = Articles.get_row_index_for_article(article_id, inventory)
            stock = int(inventory.cell(article_index, 5).value)
            new_stock_level = stock - rows[3]
            inventory.update_cell(article_index, 5, new_stock_level)

        print("Order registered.")


def register_order():
    order_id = generate_order_id()
    build_order(order_id)
    register_order_end_menu()


def display_orders_by_date():
    # ask for valid start date
    start_date = get_date("start")
    # ask for valid end date, on or later than start date
    while True:
        end_date = get_date("end")
        if end_date < start_date:
            print(
                "End date has to be a date which is the same or later than the start date"
            )
            continue
        else:
            break
    # check if there is no orders for requested period:
    registered_dates = orders.col_values(2)
    registered_dates.pop(0)
    data_exists = False
    for reg_date in registered_dates:
        if reg_date >= start_date and reg_date <= end_date:
            data_exists = True
    if data_exists:
        if start_date == end_date:
            print(f"Displaying orders from {start_date}:")
        else:
            print(f"Displaying orders from {start_date} until {end_date}:")

        start_index = Orders.get_first_row_index_for_date(start_date, orders)
        end_index = Orders.get_last_row_index_for_date(end_date, orders)
        orders_data = Orders.get_order_rows_for_dates(orders, start_index, end_index)
        display_data(orders_data[0], orders_data[1])
        display_orders_by_date_end_menu()
    else:
        print("No orders to display for your chosen dates")


def lookup_order_by_id():
    # get order id until valid
    order_id = get_order_id()
    # check if it exists
    order_nr_column = orders.col_values(1)
    order_nr_column.pop(0)
    order_rows = []
    for index, cell_value in enumerate(order_nr_column):
        if str(cell_value) == order_id:
            row_values = orders.row_values(index + 2)
            order_rows.append(row_values)

    if order_rows != []:
        print(f"Order ID {order_id}:")
        headers = orders.row_values(1)
        display_data(headers, order_rows)
        total_order_sum = 0
        total_order_quantity = 0
        for rows in order_rows:
            total_order_sum += float(rows[4])
            total_order_quantity += int(rows[3])
        print(
            f"""Total order sum: {round(total_order_sum, 2)}
Total order quantity: {total_order_quantity}
"""
        )

    else:
        print(f"There is no order with id {order_id} in the system.")

    lookup_order_end_menu()


def sales_menu():
    """
    Displays the sales menu
    """
    options = [
        "Display orders (by date)",
        "Look up order by ID",
        "Register an order",
        "Back to main menu",
    ]
    terminal_menu = TerminalMenu(options, title="Sales menu")
    menu_index = terminal_menu.show()

    match menu_index:
        case 0:
            print("Display orders (by date)")
            display_orders_by_date()
        case 1:
            print("Look up order by ID")
            lookup_order_by_id()
        case 2:
            print("Register an order")
            register_order()
        case 3:
            main_menu()


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
            display_full_sheet(inventory)
            back_to_main_menu()
        case 1:
            print("Looking up article")
            look_up_article()
        case 2:
            print("Adding article")
            build_article()
        case 3:
            print("Editing article")
            edit_article()
        case 4:
            print("Deleting article")
            delete_article()
        case 5:
            print("Back to main menu")
            main_menu()


def main_menu():
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
            sales_menu()
        case 2:
            print("Quitting program")
            SystemExit


def main():
    """Main function"""
    print("Welcome to shop register!")
    main_menu()


main()
