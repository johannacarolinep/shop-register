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

    @classmethod
    def get_row_for_article(self, inventory, article_number):
        headers = inventory.row_values(1)
        column = inventory.col_values(1)
        for index, cell_value in enumerate(column):
            if str(cell_value) == str(article_number):
                row_values = inventory.row_values(index + 1)
                return [headers, row_values]

    @classmethod
    def remove_row(self, article_nr, sheet):
        article_str = str(article_nr)
        column = sheet.col_values(1)
        index = column.index(article_str) + 1
        sheet.delete_rows(index)

    @classmethod
    def get_row_index_for_article(self, article_number, sheet):
        article_str = str(article_number)
        column = sheet.col_values(1)
        index = column.index(article_str) + 1
        return index
