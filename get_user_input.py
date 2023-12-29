import re
from datetime import datetime
from simple_term_menu import TerminalMenu
from colorama import Fore, Style
from validators import Validators

data_validator = Validators()


def get_quantity():
    """
    Runs a while loop to collect a valid quantity from the user.
    Needs to be a positive integer number.
    If quantity larger than 1000, confirm with user.

    Returns:
    int: the quantity
    """
    while True:
        quantity = input("Enter quantity, a positive integer, e.g. 17 or 2:\n")
        # if input is valid format for quantity
        if data_validator.validate_quantity(quantity):
            quantity = int(quantity)
            # if quantity is very large, does extra confirmation with user
            if quantity >= 1000:
                if confirm_user_entry(quantity):
                    break
                else:
                    print("Not registering quantity")
                    continue
            break
    return quantity


def get_sales_quantity(sheet, article_number, order) -> int:
    """
    Looks up the stock quantity for a given article.
    Iterates the given order, and decrements stock quantity if order already
    contains rows with given article. Runs a while loop to collect a sales
    quantity from the user. Has to be <= stock quantity.

    Parameters:
    - sheet (Worksheet): The sheet to reference
    - article_number (int): The article
    - order (list): The current order (existing order rows)

    Returns:
    int: The sales quantity
    """
    from articles import Articles

    article_index = Articles.get_row_index_for_article(article_number, sheet)
    stock_quantity_str = sheet.cell(article_index, 5).value
    stock_quantity = int(stock_quantity_str)
    # decrease stock quantity if current order already contains article
    for rows in order:
        if rows[2] == article_number:
            stock_quantity -= rows[3]
    # check if stock_quantity is 0
    if stock_quantity == 0:
        return 0
    # ask for sales quantity until valid input
    while True:
        sales_quantity = input(
            f"Enter sales quantity (Current stock level: {stock_quantity}):\n"
        )
        if data_validator.validate_quantity(sales_quantity):
            sales_quantity = int(sales_quantity)
            if sales_quantity <= stock_quantity:
                break
            else:
                print(
                    Fore.RED
                    + "Sales quantity cannot be more than current stock"
                    + Style.RESET_ALL
                )
                continue
        else:
            print(
                Fore.RED
                + "Input is not a valid quantity. Please try again"
                + Style.RESET_ALL
            )
            continue
    return sales_quantity


def get_price(type) -> float:
    """
    Runs a while loop to collect a valid price from the user, a positive
    decimal number. Asks for price in or price out based on the type parameter.
    If price > 500, confirms with user.

    Parameters:
    string: the type ("in" or "out")

    Returns:
    float: the price
    """
    while True:
        if type == "in":
            price = input(
                "Enter price in, a positive decimal value, e.g. 10.99:\n",
            )
        else:
            price = input(
                "Enter price out, a positive decimal value, e.g. 10.99:\n",
            )
        # check if input is valid format for price
        if data_validator.validate_price(price):
            price = round(float(price), 2)
            # if price large, confirm with user
            if price >= 500:
                if confirm_user_entry(price):
                    break
                else:
                    print("Not registering price")
                    continue
            break
    return price


def get_article_number() -> int:
    """
    Runs a while loop to collect a valid article nr from the user.
    Needs to be a positive 4 digit integer number (1000 - 9999).

    Returns:
    - int: the article nr
    """
    while True:
        article_nr = input("Enter article nr, a 4 digit number, e.g. 1001:\n")
        if data_validator.validate_article_nr(article_nr):
            article_nr = int(article_nr)
            break
    return article_nr


def get_order_id() -> str:
    """
    Runs a while loop to collect a valid order nr from the user.
    Needs to be a positive 5 digit integer number (10000-99999).

    Returns:
    - string: the order nr
    """
    while True:
        order_id = input("Enter order ID, a 5 digit number, eg 10001:\n")
        if data_validator.validate_order_nr(order_id):
            break
    return order_id


def get_article_name() -> str:
    """
    Runs a while loop to collect a valid name from the user.
    Needs to be a string of length 5-90 and contain letters.
    Can contain a number of max 2 digits, special characters !/./,/-, and
    spaces.

    Returns:
    - string: the article name, in uppercase and stripped of any extra spaces
    """
    while True:
        print(
            f"""Article names are of length 5-90 characters.
Special characters not allowed, with exception of '!/./,/-'.
Spaces are allowed, but superflous spaces will be removed.
You can one 2-digit number."""
        )
        name = input("Enter article name:\n")
        if data_validator.validate_is_name(name):
            cleaned_name = re.sub(r"\s+", " ", name).strip()
            uppercase_name = cleaned_name.upper()
            break
    return uppercase_name


def get_date(type) -> str:
    """
    Runs a while loop to collect a valid date from the user. Asks for start/end
    date depending on the type parameter.
    Needs to be a string matching YYYY-MM-DD, a real date (eg not 31st of
    February), and cannot be a future date.

    Parameters:
    - type (string): The type of date, "start" or "end".

    Returns:
    - string: the date
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    while True:
        if type == "start":
            print("\nPlease enter a START date")
        elif type == "end":
            print("\nPlease enter an END date")
        print(
            f"""- Today is: {current_date}. Please don't enter a future date.
- Format should be YYYY-MM-DD"""
        )
        date = input("Enter date here:\n")
        # break if validation returns true
        if data_validator.validate_is_date(date):
            break
    return date


def confirm_user_entry(user_entry) -> bool:
    """
    Uses a simple terminal menu to confirm user entry with user.

    Parameter:
    - user_entry (string): The value to confirm

    Returns:
    - bool: True if user answers yes, otherwise false
    """
    options = ["Yes", "No"]
    terminal_menu = TerminalMenu(
        options, title=f"You entered {user_entry}. Are you sure?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Yes":
        return True
    else:
        return False


def confirm_order_complete() -> bool:
    """
    Ask user if they want to add another row to sales order

    Returns:
    bool: True if user confirms order is complete, False if user chose to add
    more rows
    """
    options = ["Add row to sales order", "Order is complete"]
    terminal_menu = TerminalMenu(
        options, title="\nDo you want to add more articles to this order?"
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Add row to sales order":
        return False
    elif options[confirm_response] == "Order is complete":
        return True


def confirm_order_final() -> bool:
    """
    Ask user if they want to finalize the sales order

    Returns:
    bool: True if user chooses "Finalize order", False if user chooses
    "Cancel order"
    """
    options = ["Finalize order", "Cancel order"]
    terminal_menu = TerminalMenu(
        options,
        title="Select 'Finalize order' to add it to the system.",
    )
    confirm_response = terminal_menu.show()
    if options[confirm_response] == "Finalize order":
        return True
    elif options[confirm_response] == "Cancel order":
        return False
