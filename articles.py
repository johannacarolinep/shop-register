import os
from simple_term_menu import TerminalMenu
from get_user_input import (
    get_article_number,
    get_article_name,
    get_price,
    get_quantity,
    confirm_user_entry,
)
from helpers import display_data, add_row
from validators import Validators

data_validator = Validators()


class Articles:
    """
    Represents an inventory management class for articles.

    Attributes:
    - article (int): The unique identifier for the article.
    - article_name (str): The name of the article.
    - price_in (float): The cost of purchasing the article.
    - price_out (float): The selling price of the article.
    - article_quantity (int): The stock quantity of the article.

    Methods:
    - to_row(): Converts the article information to a list.
    - get_row_for_article(inventory, article_number): Retrieves a row of
    information for a specific article from the inventory sheet
    - remove_row(article_nr, sheet): Removes a row corresponding to the given
    article number from the sheet.
    - get_row_index_for_article(article_number, sheet): gets the row index for
    a specific article from the sheet
    - look_up_article(inventory): Gets an article number from the user and
    looks for it in the inventory. If found, prints its row in a table format.
    - edit_article(inventory, article=None): Asks for an article nr if none
    provided. Confirms user wants to edit the article, and calls the edit_menu
    method.
    - edit_menu(article, inventory): Displays a menu for editing one or more
    attributes of an article. Handles the user's choice, and updates the
    inventory sheet accordingly.
    - delete_article(inventory, inactive_articles): confirms with user which
    article to delete, then moves the article from the inventory to the
    inactive_articles sheet
    - build_article(inventory, inactive_articles): Adds a new article to the
    inventory by collecting data from the user, or redirects user to edit the
    article if the article number already exists.
    """

    def __init__(
        self,
        article,
        article_name,
        price_in,
        price_out,
        article_quantity,
    ):
        """
        Initializes a new Articles instance.

        Parameters:
        - article (int): The unique identifier for the article.
        - article_name (str): The name of the article.
        - price_in (float): The cost of purchasing the article.
        - price_out (float): The selling price of the article.
        - article_quantity (int): The stock quantity of the article.
        """
        self.article = article
        self.article_name = article_name
        self.price_in = price_in
        self.price_out = price_out
        self.article_quantity = article_quantity

    def to_row(self):
        """
        Converts the article information to a list.

        Returns:
        list: A list containing [article, article_name, price_in, price_out,
        article_quantity].
        """
        return [
            self.article,
            self.article_name,
            self.price_in,
            self.price_out,
            self.article_quantity,
        ]

    @classmethod
    def get_row_for_article(self, inventory, article_number):
        """
        Retrieves a row of information for a specific article from the
        inventory sheet.

        Parameters:
        - inventory: The inventory sheet.
        - article_number (int): The article number to look for.

        Returns:
        list: A list containing the headers and row values for the article.
        """
        headers = inventory.row_values(1)
        column = inventory.col_values(1)
        for index, cell_value in enumerate(column):
            if str(cell_value) == str(article_number):
                row_values = inventory.row_values(index + 1)
                return [headers, row_values]

    @classmethod
    def remove_row(self, article_nr, sheet):
        """
        Finds the row of a given article number in a sheet, and removes  it.

        Parameters:
        - article_nr (int): The identifier of the article to remove
        - sheet: The sheet from which the row will be removed
        """
        article_str = str(article_nr)
        column = sheet.col_values(1)
        index = column.index(article_str) + 1
        sheet.delete_rows(index)

    @classmethod
    def get_row_index_for_article(self, article_number, sheet):
        """
        Finds the row index for a specific article from the provided sheet.

        Parameters:
        - article_number (int): The article number to look for.
        - sheet: The sheet in which to look.

        Returns:
        int: The row index for the specified article.
        """
        article_str = str(article_number)
        column = sheet.col_values(1)
        index = column.index(article_str) + 1
        return index

    @classmethod
    def look_up_article(self, inventory):
        """
        Gets an article number from user and looks for it in the inventory
        If found, prints its row in a table format.

        Parameters:
        - inventory: The inventory sheet.
        """
        print(
            f"""LOOK UP ARTICLES

    Search for articles in the inventory (by article number)
    --------------------------------------------
    """
        )
        article_number = get_article_number()
        # checks if article_number exists in sheet
        if data_validator.validate_article_exists(
            article_number,
            inventory,
        ):
            row_data = self.get_row_for_article(inventory, article_number)
            # prints table of the article
            print(f"\nArticle {article_number}:")
            display_data(row_data[0], [row_data[1]])
            print("")
        else:
            print("\nArticle not found.\n")

    @classmethod
    def edit_article(self, inventory, article=None):
        """
        If article nr is not provided, asks user for one. Checks if the
        article exists, displays its details, and asks if the user wants to
        edit it. If confirmed, calls edit_menu method.

        Parameters:
        - inventory: The inventory sheet.
        - article (optional): The article number to edit.
        """
        print(
            f"""EDIT ARTICLES

Search for articles in the inventory (by article number).
Edit article name, price in, price out, and/or stock quantity.
--------------------------------------------
"""
        )
        # get article nr from user if none provided
        if not article:
            article = get_article_number()

        if data_validator.validate_article_exists(article, inventory):
            # if article found in inventory, display it and confirm intent
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
                # if user confirmed, call edit_menu method
                self.edit_menu(article, inventory)
        else:
            print("Article not found.")

    @classmethod
    def edit_menu(self, article, inventory):
        """
        Displays a menu for editing one or more attributes of an article.
        Handles the user's choice to edit the name, price in, price out,
        and/or stock. Updates the inventory sheet accordingly.

        Parameters:
        - article: The article number, identifier for the article to edit.
        - inventory: The inventory sheet.
        """
        options = ["Name", "Price_in", "Price_out", "Stock"]
        terminal_menu = TerminalMenu(
            options,
            multi_select=True,
            show_multi_select_hint=True,
            multi_select_select_on_accept=False,
            multi_select_empty_ok=True,
            title=f"Which attributes would you like to edit?",
        )
        response = terminal_menu.show()
        if response is None:
            print("You did not make a selection.")
        else:
            # store user's selection of attributes to edit
            response_array = list(terminal_menu.chosen_menu_entries)
            row_index = Articles.get_row_index_for_article(article, inventory)
            # ask for new value and update sheet if attribute in user selection
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
                # ask for new price_out until it's greater than price_in
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

    @classmethod
    def delete_article(self, inventory, inactive_articles):
        """
        Asks the user for an article number to delete. Looks for the article in
        the inventory. If found, displays it and asks for confirmation.
        If confirmed, deletes the row from the inventory sheet, and adds it to
        the inactive_articles sheet.

        Parameters:
        - inventory: The inventory sheet.
        - inactive_articles: The sheet for inactive articles.
        """
        article = get_article_number()
        if data_validator.validate_article_exists(article, inventory):
            print("Article to remove:")
            row_data = Articles.get_row_for_article(inventory, article)
            # display the article and confirm deletion with user
            display_data(row_data[0], [row_data[1]])
            options = ["Yes", "No"]
            terminal_menu = TerminalMenu(
                options,
                title=f"Would you like to delete this article?",
            )
            response = terminal_menu.show()
            if options[response] == "Yes":
                # add article to inactive_articles sheet
                add_row(row_data[1], inactive_articles)
                # remove article from inventory sheet
                Articles.remove_row(article, inventory)
                print("Article removed")
            else:
                print("Cancelled.")
        else:
            print("Article not found.")

    @classmethod
    def build_article(self, inventory, inactive_articles):
        """
        Adds a new article to the inventory by collecting data from the user.
        If provided article nr already exists, asks user if they instead want
        to edit the article.

        Parameters:
        - inventory: The inventory sheet.
        - inactive_articles: The sheet for inactive articles.

        Returns:
        bool: True if reaching end of build article, False if user is
        redirected to edit article.
        """
        print(
            f"""ADD ARTICLES

    Add a new article to the inventory.
    --------------------------------------------
    """
        )
        article = get_article_number()
        # if article nr belongs to an inactive article, print message
        if data_validator.validate_article_exists(article, inactive_articles):
            print(
                f"""Article with ID {article} already exists and is inactive. Please choose a different article number."""
            )
        else:
            # if article nr exists in inventory, offer to edit existing article
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
                    return False
                else:
                    os.system("clear")
                    return True
            else:
                print("\nStarting article creation")
                # display progress, article with empty values
                headers = inventory.row_values(1)
                temp_row = [[str(article), "-", "-", "-", "-"]]
                display_data(headers, temp_row)
                # get article name from user
                temp_row[0][1] = get_article_name()
                display_data(headers, temp_row)
                # get price in from user
                temp_row[0][2] = get_price("in")
                display_data(headers, temp_row)
                # ask user for price out until it's greater than price in
                user_confirm = False
                while not user_confirm:
                    temp_row[0][3] = get_price("out")
                    if temp_row[0][3] < temp_row[0][2]:
                        print("Price out is lower than price in.")
                        user_confirm = confirm_user_entry(temp_row[0][3])
                    else:
                        user_confirm = True
                display_data(headers, temp_row)
                # get quantity/stock from user
                temp_row[0][4] = get_quantity()
                print("\nFinished article:")
                display_data(headers, temp_row)
                # create the article and add it to the inventory sheet
                article_instance = Articles(
                    article,
                    temp_row[0][1],
                    temp_row[0][2],
                    temp_row[0][3],
                    temp_row[0][4],
                )
                article_row = article_instance.to_row()
                add_row(article_row, inventory)
                return True
