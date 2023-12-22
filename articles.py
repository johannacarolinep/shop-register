class Articles:
    def __init__(self, article, article_name, price_in, price_out, article_quantity):
        self.article = article
        self.article_name = article_name
        self.price_in = price_in
        self.price_out = price_out
        self.article_quantity = article_quantity

    def to_row(self):
        return [
            self.article,
            self.article_name,
            self.price_in,
            self.price_out,
            self.article_quantity,
        ]
