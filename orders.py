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
