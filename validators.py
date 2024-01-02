import re
from datetime import datetime
from colorama import Fore, Style


class Validators:
    """
    A class of validators for input.

    Methods:
    - validate_not_empty(data) -> bool: Validates data is not empty.
    - validate_is_positive(data) -> bool: Validates data is a positive number.
    - validate_is_int(data) -> bool: Validates data can be parsed to an
    integer.
    - validate_is_float(data) -> bool: Validates data can be parsed to a float.
    - validate_article_exists(article_number, sheet) -> bool: Validates if an
    article number exists in the first column of a sheet.
    - validate_price(data) -> bool: Validates if data (user input) has the
    right format and a valid value for a price.
    - validate_quantity(data) -> bool: Validates if data (user input) has the
    right format and a valid value for a quantity.
    - validate_article_number(data) -> bool: Validates if data (user input) has
    the right format for an article number.
    - validate_is_name(data) -> bool: Validates if data (user input) has the
    right format for an article name.
    - validate_is_date(date_str) -> bool: Validates if a string is a valid date
    in the format YYYY-MM-DD.
    - validate_order_number(data) -> bool: Validates if data (user input) has
    the correct format for an order number.
    """

    def validate_not_empty(self, data) -> bool:
        """
        Validates data is not empty.

        Parameters:
        data (string): the user input to check

        Returns:
        bool: True if data exists, else False
        """
        if not data:
            print(
                Fore.RED
                + "Invalid: You submitted an empty input. Please try again."
                + Style.RESET_ALL
            )
            return False
        else:
            return True

    def validate_is_positive(self, data) -> bool:
        """
        Validates data is a positive number.

        Parameters:
        data (string): the user input to check

        Returns:
        bool: True if data data can be parsed to a positive float, else False
        """
        try:
            temp_float = float(data)
            if temp_float <= 0:
                raise ValueError("Data must be a positive value.")
        except ValueError as e:
            print(
                Fore.RED + f"Invalid: {e} Please try again." + Style.RESET_ALL,
            )
            return False
        return True

    def validate_is_int(self, data) -> bool:
        """
        Validates data can be parsed to an integer.

        Parameters:
        data (string): the user input to check

        Returns:
        bool: True if data can be parsed to an integer, else False
        """
        try:
            temp_int = int(data)
        except ValueError:
            print(
                Fore.RED
                + "Invalid input. Data must be an integer. Please try again"
                + Style.RESET_ALL
            )
            return False
        return True

    def validate_is_float(self, data) -> bool:
        """
        Validates data can be parsed to a float.

        Parameters:
        data (string): the user input to check

        Returns:
        bool: True if data can be parsed to a float, else False
        """
        try:
            temp_float = float(data)
        except ValueError:
            print(
                Fore.RED
                + "Invalid. Data must be a decimal number. Please try again"
                + Style.RESET_ALL
            )
            return False
        return True

    def validate_article_exists(self, article_number, sheet) -> bool:
        """
        Validates if an article number exists in the first column of a sheet.

        Parameters:
        article_number (int): the article number to look for
        sheet (Worksheet): the worksheet to look in

        Returns:
        bool: True if article number is found, else False
        """
        column = sheet.col_values(1)
        if str(article_number) in column:
            return True
        else:
            return False

    def validate_price(self, data) -> bool:
        """
        Validates if data (user input) has the right format for a price;
        is not empty, can be parsed to a float, and is positive.
        Validates if data has a valid value for a price;
        should be less or equal to 99999.99.

        Parameters:
        data (str): the input to check

        Returns:
        bool: True if input has format and value of price, else False
        """
        if (
            self.validate_not_empty(data)
            and self.validate_is_float(data)
            and self.validate_is_positive(data)
        ):
            temp_price = float(data)
            if temp_price <= 99999.99:
                return True
            else:
                print(
                    Fore.RED
                    + f"""
Sorry, the entered value is above the upper limit for a price.
You entered {temp_price}. The upper limit is 99999.99. Try again."""
                )
                return False
        else:
            return False

    def validate_quantity(self, data) -> bool:
        """
        Validates if data (user input) has the right format for a quantity;
        is not empty, can be parsed to an integer, and is positive.
        Validates if data has a valid value for a quantity;
        should be less than 1000000.

        Parameters:
        data (str): the input to check

        Returns:
        bool: True if input has format and value of quantity, else False
        """
        if (
            self.validate_not_empty(data)
            and self.validate_is_int(data)
            and self.validate_is_positive(data)
        ):
            temp_quantity = int(data)
            if temp_quantity < 1000000:
                return True
            else:
                print(
                    Fore.RED
                    + f"""
Sorry, the entered value is above the upper limit for a quantity.
You entered {temp_quantity}. The upper limit is 999999. Try again."""
                )
        else:
            return False

    def validate_article_number(self, data) -> bool:
        """
        Validates if data (user input) has the right format for an article
        number; is not empty, is positive, and is in the range 1000 - 9999.

        Parameters:
        data (str): the input to check

        Returns:
        bool: True if input has format of an article number, else False
        """
        if (
            self.validate_not_empty(data)
            and self.validate_is_int(data)
            and self.validate_is_positive(data)
        ):
            try:
                temp_int = int(data)
                # checks if outside of scope for art. numbers
                if temp_int > 9999 or temp_int < 1000:
                    raise ValueError("Must be a positive 4 digit integer.")
            except ValueError as e:
                print(
                    Fore.RED
                    + f"Invalid input: {e} Please try again."
                    + Style.RESET_ALL,
                )
                return False
            return True

    def validate_is_name(self, data) -> bool:
        """
        Validates if data (user input) has the right format for an article
        name; is not empty, once stripped of extra spaces, has length of 5-34
        characters,

        Parameters:
        data (str): the input to check

        Returns:
        bool: True if input has format of an article number, else False
        """
        if self.validate_not_empty(data):
            # Remove trailing whitespaces and extra whitespaces
            cleaned_str = re.sub(r"\s+", " ", data).strip()
            try:
                # Check the maximum and minimum length
                if len(cleaned_str) > 34:
                    raise ValueError("The max length is 34 characters.")
                if len(cleaned_str) < 5:
                    raise ValueError("The minimum length is 5 characters")
                # Check data has letters and optional max 2 digit number
                pattern = re.compile(
                    r"(?:[a-zA-Z0-9\s.,!-]*[a-zA-Z]+\s*\d{0,2}\s*"
                    r"[a-zA-Z0-9\s.,!-]*)+"
                )
                if bool(pattern.search(cleaned_str)) is False:
                    raise ValueError("Format incorrect.")
            except ValueError as e:
                print(
                    Fore.RED
                    + f"Invalid input: {e}.\nPlease try again."
                    + Style.RESET_ALL
                )
                return False
            return True

    def validate_is_date(self, date_str) -> bool:
        """
        Validates if a string is a valid date: has format YYYY-MM-DD and is a
        real date (eg not 31st of February).

        Parameters:
        date_str (str): the string to check

        Returns:
        bool: True if date_str is a valid date, else False
        """
        if self.validate_not_empty(date_str):
            # strip trailing whitespaces and check format is correct
            date_str = date_str.strip()
            pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            if pattern.match(date_str):
                # if correct format, check if it can be parsed to a date object
                date_format = "%Y-%m-%d"
                try:
                    date_to_check = datetime.strptime(date_str, date_format)
                    current_date = datetime.now()
                    # check that it is not a future date
                    if date_to_check <= current_date:
                        return True
                    else:
                        print(
                            Fore.RED
                            + "Date cannot be greater than current date."
                            + Style.RESET_ALL
                        )
                        return False
                except ValueError:
                    print(
                        Fore.RED
                        + "Date provided does not exist. Please try again."
                        + Style.RESET_ALL
                    )
                    return False
            else:
                print(
                    Fore.RED
                    + "Invalid format. Format must be YYYY-MM-DD. Try again."
                    + Style.RESET_ALL,
                )
                return False

    def validate_order_number(self, data) -> bool:
        """
        Validates if data (user input) has correct format for an order number:
        is not empty, can be parsed to an integer, is positive, and in the
        right range 10000-99999.

        Parameters:
        date (str): the string to check

        Returns:
        bool: True if data is a valid order number, else False
        """
        if (
            self.validate_not_empty(data)
            and self.validate_is_positive(data)
            and self.validate_is_int(data)
        ):
            try:
                temp_int = int(data)
                # checks if outside of scope for art. numbers
                if temp_int > 99999 or temp_int < 10000:
                    raise ValueError("Must be a positive 5 digit integer.")
            except ValueError as e:
                print(
                    Fore.RED
                    + f"Invalid input: {e} Please try again.\n"
                    + Style.RESET_ALL,
                )
                return False
            return True
