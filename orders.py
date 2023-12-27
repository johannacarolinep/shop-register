from datetime import datetime


class Orders:
    def __init__(self, order_number, article_number, quantity, sum):
        self.order_number = order_number
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.article_number = article_number
        self.quantity = quantity
        self.sum = sum

    def to_row(self):
        return [
            self.order_number,
            self.date,
            self.article_number,
            self.quantity,
            self.sum,
        ]

    @classmethod
    def get_first_row_index_for_date(self, date_str, sheet):
        column = sheet.col_values(2)
        index = column.index(date_str) + 1
        return index

    @classmethod
    def get_last_row_index_for_date(self, date_str, sheet):
        column = sheet.col_values(2)
        index = len(column) - 1 - column[::-1].index(date_str)
        return index + 1

    @classmethod
    def get_order_rows_for_dates(self, orders, start_index, end_index):
        headers = orders.row_values(1)
        orders_range = "A" + str(start_index) + ":E" + str(end_index)
        rows = orders.get(orders_range)

        return [headers, rows]
