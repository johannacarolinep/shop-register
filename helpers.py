from prettytable import PrettyTable

pretty_table = PrettyTable()


def add_row(row, sheet):
    sheet.append_row(row)


def display_full_sheet(sheet):
    data = sheet.get_all_values()
    headers = data[0]
    data.pop(0)
    display_data(headers, data)


def display_data(headers, rows):
    """
    Display data from sheet
    """
    pretty_table.field_names = headers
    pretty_table.add_rows(rows)
    print(pretty_table)
    pretty_table.clear_rows()
