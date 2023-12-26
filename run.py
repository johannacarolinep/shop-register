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
from articles import Articles
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
# print(data)


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
        else:
            main_menu()
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
        return article_instance.to_row()


def add_row(row, sheet):
    sheet.append_row(row)


def delete_article():
    article = get_article_number()
    if data_validator.validate_article_existence(article, inventory):
        # display row
        print("Article to remove:")
        row_data = get_row_for_article(article)
        display_data(row_data[0], [row_data[1]])
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(
            options,
            title=f"Would you like to delete this article?",
        )
        response = terminal_menu.show()
        if options[response] == "Yes":
            remove_row(article, inventory)
        else:
            print("Cancelled. Routing back to main menu")
            main_menu()
    else:
        print("Article not found. Routing back to main menu")
        main_menu()


def remove_row(article_nr, sheet):
    article_str = str(article_nr)
    column = sheet.col_values(1)
    index = column.index(article_str) + 1
    sheet.delete_rows(index)


def display_data(headers, rows):
    """
    Display data from sheet
    """
    pretty_table.field_names = headers
    pretty_table.add_rows(rows)
    print(pretty_table)
    pretty_table.clear_rows()


def display_full_sheet(sheet):
    data = sheet.get_all_values()
    headers = data[0]
    data.pop(0)
    display_data(headers, data)


def look_up_article():
    article_number = get_article_number()
    if data_validator.validate_article_existence(article_number, inventory):
        row_data = get_row_for_article(article_number)
        display_data(row_data[0], [row_data[1]])
    else:
        print("Article not found. Re-routing to main menu.")
        main_menu()


def get_row_for_article(article_number):
    headers = inventory.row_values(1)
    column = inventory.col_values(1)
    for index, cell_value in enumerate(column):
        if str(cell_value) == str(article_number):
            row_values = inventory.row_values(index + 1)
            return [headers, row_values]


def get_row_index_for_article(article_number):
    article_str = str(article_number)
    column = inventory.col_values(1)
    index = column.index(article_str) + 1
    return index


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
        main_menu()
    else:
        response_array = list(terminal_menu.chosen_menu_entries)
        print("Response array", response_array)
        row_index = get_row_index_for_article(article)

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

        main_menu()


def edit_article():
    article = get_article_number()
    if data_validator.validate_article_existence(article, inventory):
        # display row
        print("Article to edit:")
        row_data = get_row_for_article(article)
        display_data(row_data[0], [row_data[1]])
        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(
            options,
            title=f"Would you like to edit this article?",
        )
        response = terminal_menu.show()
        if options[response] == "Yes":
            print("opening multi option menu")
            edit_menu(article)
        else:
            print("Cancelled. Routing back to main menu")
            main_menu()
    else:
        print("Article not found. Routing back to main menu")
        main_menu()


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
            display_full_sheet(inventory)
            back_to_main_menu()
        case 1:
            print("Looking up article")
            look_up_article()
        case 2:
            print("Adding article")
            article_row = build_article()
            add_row(article_row, inventory)
        case 3:
            print("Editing article")
            edit_article()
        case 4:
            print("Deleting article")
            delete_article()
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
