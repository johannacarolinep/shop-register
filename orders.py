from datetime import datetime


class Orders:
    """
    Represents a class for managing orders.

    Attributes:
    - order_number (int): The unique identifier for the complete order (which
    can consist of several order rows).
    - date (str): The date the order was registered, formatted as "YYYY-MM-DD".
    - article_number (int): The unique identifier for the article
    associated with the order.
    - quantity (int): The sales quantity of the order row (one article per row)
    - sum (float): The sum of the order row (not necessarily for the complete
    order).

    Methods:
    - to_row(): Converts the order information to a list.
    - get_first_row_index_for_date(date_str, sheet): Finds the first row index
    for a specific date, or the first date following that date, from the sheet.
    - get_last_row_index_for_date(date_str, sheet): Finds the last row index
    for a specific date, or the first date preceding that date, from the sheet.
    - get_order_rows_for_dates(orders, start_index, end_index): Retrieves order
    rows within a specified range from the orders sheet.
    """

    def __init__(self, order_number, article_number, quantity, sum):
        """
        Initializes a new Orders instance.

        Parameters:
        - order_number (int): The unique identifier for the complete order
        (which can consist of several order rows).
        - article_number (int): The unique identifier for the article
        - quantity (int): The sales quantity of the order row (one article)
        - sum (float): The sum of the order row (not necessarily for the
        complete order).
        """
        self.order_number = order_number
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.article_number = article_number
        self.quantity = quantity
        self.sum = sum

    def to_row(self):
        """
        Converts the order information to a row for easy storage or display.

        Returns:
        list: A list containing [order_number, date, article_number, quantity,
        sum].
        """
        return [
            self.order_number,
            self.date,
            self.article_number,
            self.quantity,
            self.sum,
        ]

    @classmethod
    def get_first_row_index_for_date(self, date_str, sheet):
        """
        Finds the first row index for a specific date, or if there is no exact
        match for the provided date, the first date following that date,
        from the sheet.

        Parameters:
        - date_str (str): The date for which to find the first row.
        - sheet: The sheet containing the order rows

        Returns:
        int: The first row index for the date.
        """
        column = sheet.col_values(2)
        column.pop(0)
        for item in column:
            if item >= date_str:
                date_str = item
                break
        index = column.index(date_str) + 2
        return index

    @classmethod
    def get_last_row_index_for_date(self, date_str, sheet):
        """
        Finds the last row index for a specific date, or if there is no exact
        match for the provided date, the first date preceding that date,
        from the sheet.

        Parameters:
        - date_str (str): The date for which to find the last row.
        - sheet: The sheet containing the order rows.

        Returns:
        int: The last row index for the specified date.
        """
        column = sheet.col_values(2)
        column.pop(0)
        for item in column:
            if item <= date_str:
                temp_date = item
        index = len(column) - 1 - column[::-1].index(temp_date)
        return index + 2

    @classmethod
    def get_order_rows_for_dates(self, orders, start_index, end_index):
        """
        Retrieves order rows within a specified range from the orders sheet.

        Parameters:
        - orders: The orders sheet.
        - start_index (int): The starting row index.
        - end_index (int): The ending row index.

        Returns:
        list: A list containing the headers and rows for the requested range.
        """
        headers = orders.row_values(1)
        orders_range = "A" + str(start_index) + ":E" + str(end_index)
        rows = orders.get(orders_range)
        return [headers, rows]
