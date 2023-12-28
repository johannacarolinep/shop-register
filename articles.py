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
