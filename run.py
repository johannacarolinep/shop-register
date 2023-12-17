import gspread
from google.oauth2.service_account import Credentials
from simple_term_menu import TerminalMenu

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
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
        quantity = input("Enter quantity, a positive integer number, e.g. 17\n")

        if validate_quantity(quantity):
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



def validate_quantity(data):
    """
    Validates data, returns true if data is a positive integer value.
    """
    try:
        # checks if empty
        if not data:
            raise ValueError("Data cannot be empty. Please try again.")
        
        # tries to convert to int
        quantity = int(data)

        # checks if <= 0
        if quantity <= 0:
            raise ValueError(f"Quantity must be a positive integer value. Please try again")
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            print("Invalid input. Quantity must be a positive integer. Please try again")
        else:
            print(f"Invalid: {e} Please try again.\n")
        
        return False
    
    return True


def confirm_user_entry(user_entry):
    """
    Uses a simple terminal menu to confirm user entry with user. Returns true if user answers yes.
    """
    options = ["Yes", "No"]
    terminal_menu = TerminalMenu(options, title=f"You entered {user_entry}. Are you sure?")
    confirm_response = terminal_menu.show()
    
    if options[confirm_response] == "Yes":
        return True
    else:
        return False
    


quantity = get_quantity()
print(f"Quantity is: {quantity}")
print(f"Quantity is of type {type(quantity)}")