import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu
from validators import Validators
import re

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

# inventory = SHEET.worksheet("inventory")
# data = inventory.get_all_values()
# print(data)


def get_quantity():
    """
    Get a quantity from the user. Runs a while loop to collect a valid quantity
    from the user. Needs to be a positive integer number. If quantity larger
    than 1000, confirm with user.
    """
    while True:
        quantity = input("Enter quantity, a positive integer, e.g. 17 or 2:\n")

        if data_validator.validate_quantity(quantity):
            quantity = int(quantity)
            # if quantity is very large, does extra confirmation with user
            if quantity >= 1000:
                if confirm_user_entry(quantity):
                    print("Quantity is valid")
                    break
                else:
                    print("Not registering quantity")
                    continue
            print("Quantity is valid")
            break

    return quantity


def get_price(type):
    """
    Get a price from the user. Runs a while loop to collect a valid price
    from the user. Needs to be a positive number. If price is larger
    than 500, confirm with user.
    """
    while True:
        if type == "in":
            price = input("Enter price in, a positive decimal value, e.g. 10.99:\n")
        else:
            price = input("Enter price out, a positive decimal value, e.g. 10.99:\n")

        if data_validator.validate_price(price):
            price = round(float(price), 2)
            # if quantity is very large, does extra confirmation with user
            if price >= 500:
                if confirm_user_entry(price):
                    print("Price is valid")
                    break
                else:
                    print("Not registering price")
                    continue
            break

    return price


def get_article_number():
    """
    Get an article number from the user. Runs a while loop to collect a valid
    article nr from the user. Needs to be a positive 4 digit integer number.
    """
    while True:
        article_nr = input("Enter article nr, a 4 digit number, e.g. 1001:\n")

        if data_validator.validate_article_nr(article_nr):
            article_nr = int(article_nr)
            print("Article number is valid format")
            break

    return article_nr


def get_article_name():
    """
    Get a name from the user. Runs a while loop to collect a valid name
    from the user. Needs to be a string of max length 90.
    Has to contain letters, and a max of 2 numbers.
    """
    while True:
        print(
            "Article names are of length 5-90 characters.\n"
            "Special characters not allowed, with exception of '!/./,/-'.\n"
            "You can include up to one 2-digit number."
        )
        name = input("Enter article name:\n")

        if data_validator.validate_is_name(name):
            cleaned_name = re.sub(r"\s+", " ", name).strip()
            uppercase_name = cleaned_name.upper()
            break

    return uppercase_name


def confirm_user_entry(user_entry):
    """
    Uses a simple terminal menu to confirm user entry with user.
    Returns true if user answers yes.
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
