from datetime import datetime
from get_user_input import (
    get_date,
    get_order_id,
    get_article_number,
    get_sales_quantity,
    confirm_order_complete,
    confirm_order_final,
)
from validators import Validators
from articles import Articles
from helpers import display_data, add_row

data_validator = Validators()


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

    @classmethod
    def generate_order_id(self, orders):
        """
        Generates a new order ID based on the existing greatest order ID in the
        sheet.

        Parameters:
        - orders: The orders sheet.

        Returns:
        int: the new order ID.
        """
        current_id = orders.get_all_values()[-1][0]
        return int(current_id) + 1

    @classmethod
    def display_orders_by_date(self, orders):
        # ask for valid start date
        start_date = get_date("start")
        # ask for valid end date, on or later than start date
        while True:
            end_date = get_date("end")
            if end_date < start_date:
                print("End date has to the same as or later than the start date")
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
            orders_data = Orders.get_order_rows_for_dates(
                orders,
                start_index,
                end_index,
            )
            display_data(orders_data[0], orders_data[1])
        else:
            print("No orders to display for your chosen dates")

    @classmethod
    def lookup_order_by_id(self, orders):
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

    @classmethod
    def build_order(self, order_id, orders, inventory):
        order = []
        order_complete = False
        while not order_complete:
            # ask for article id, verify exists
            article_number = get_article_number()
            if data_validator.validate_article_existence(
                article_number,
                inventory,
            ):
                # get sales quantity from user
                sales_quantity = get_sales_quantity(
                    inventory,
                    article_number,
                    order,
                )
                # calculate sum
                article_index = Articles.get_row_index_for_article(
                    article_number, inventory
                )
                price_str = inventory.cell(article_index, 4).value
                price = float(price_str)
                sum = round(price * sales_quantity, 2)

                orders_instance = Orders(
                    order_id,
                    article_number,
                    sales_quantity,
                    sum,
                )
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
                article_index = Articles.get_row_index_for_article(
                    article_id,
                    inventory,
                )
                stock = int(inventory.cell(article_index, 5).value)
                new_stock_level = stock - rows[3]
                inventory.update_cell(article_index, 5, new_stock_level)

            print("Order registered.")
