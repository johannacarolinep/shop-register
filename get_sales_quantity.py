from colorama import Fore, Style
from validators import Validators
from articles import Articles


data_validator = Validators()


def get_sales_quantity(sheet, article_number, order) -> int:
    """
    Looks up the stock quantity for a given article.
    Iterates the given order, and decrements stock quantity if order already
    contains rows with given article. Runs a while loop to collect a sales
    quantity from the user. Has to be <= stock quantity.

    Parameters:
    - sheet (Worksheet): The sheet to reference
    - article_number (int): The article
    - order (list): The current order (existing order rows)

    Returns:
    int: The sales quantity
    """
    article_index = Articles.get_row_index_for_article(article_number, sheet)
    stock_quantity_str = sheet.cell(article_index, 5).value
    stock_quantity = int(stock_quantity_str)
    # decrease stock quantity if current order already contains article
    for rows in order:
        if rows[2] == article_number:
            stock_quantity -= rows[3]
    # check if stock_quantity is 0
    if stock_quantity == 0:
        return 0
    # ask for sales quantity until valid input
    while True:
        sales_quantity = input(
            Fore.LIGHTMAGENTA_EX
            + f"""Enter sales quantity (Current stock level: {stock_quantity}):
"""
            + Style.RESET_ALL
        )
        if data_validator.validate_quantity(sales_quantity):
            sales_quantity = int(sales_quantity)
            if sales_quantity <= stock_quantity:
                break
            else:
                print(
                    Fore.RED
                    + "Sales quantity cannot be more than current stock"
                    + Style.RESET_ALL
                )
                continue
        else:
            print(
                Fore.RED
                + "Input is not a valid quantity. Please try again"
                + Style.RESET_ALL
            )
            continue
    return sales_quantity
