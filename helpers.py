from prettytable import PrettyTable

pretty_table = PrettyTable()


def add_row(row, sheet):
    """Adds a list as a row to a sheet"""
    sheet.append_row(row)


def display_full_sheet(sheet):
    """
    Gets all data from a sheet, separates headers and rows, and passes
    them to display_data function
    """
    data = sheet.get_all_values()
    headers = data[0]
    data.pop(0)
    display_data(headers, data)


def display_data(headers, rows):
    """Displays headers and rows in a table, using pretty table"""
    pretty_table.field_names = headers
    pretty_table.add_rows(rows)
    print(pretty_table)
    pretty_table.clear_rows()
