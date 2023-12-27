import re
from datetime import datetime


class Validators:
    def validate_not_empty(self, data) -> bool:
        """
        Validates data, returns true if data exists.
        """
        try:
            if not data:
                raise ValueError("Data cannot be empty.")
        except ValueError as e:
            print(f"Invalid: {e} Please try again.\n")
            return False
        return True

    def validate_is_positive(self, data) -> bool:
        try:
            temp_float = float(data)
            if temp_float <= 0:
                raise ValueError("Data must be a positive value.")
        except ValueError as e:
            print(f"Invalid: {e} Please try again.\n")
            return False
        return True

    def validate_is_int(self, data) -> bool:
        try:
            temp_int = int(data)
        except ValueError:
            print("Invalid input. Data must be an integer. Please try again")
            return False
        return True

    def validate_is_float(self, data) -> bool:
        try:
            temp_float = float(data)
        except ValueError:
            print(
                "Invalid. Data must be a decimal number. Please try again",
            )
            return False
        return True

    def validate_article_existence(self, articleNr, sheet) -> bool:
        column = sheet.col_values(1)
        if str(articleNr) in column:
            return True
        else:
            return False

    def validate_price(self, data) -> bool:
        if (
            self.validate_not_empty(data)
            and self.validate_is_float(data)
            and self.validate_is_positive(data)
        ):
            return True
        else:
            return False

    def validate_quantity(self, data) -> bool:
        if (
            self.validate_not_empty(data)
            and self.validate_is_int(data)
            and self.validate_is_positive(data)
        ):
            return True
        else:
            return False

    def validate_article_nr(self, data) -> bool:
        if (
            self.validate_not_empty(data)
            and self.validate_is_positive(data)
            and self.validate_is_int(data)
        ):
            try:
                temp_int = int(data)
                # checks if outside of scope for art. numbers
                if temp_int > 9999 or temp_int < 1000:
                    raise ValueError("Must be a positive 4 digit integer.")
            except ValueError as e:
                print(f"Invalid: {e} Please try again.\n")
                return False
            return True

    def validate_is_name(self, data) -> bool:
        if self.validate_not_empty(data):
            # Remove trailing whitespaces and extra whitespaces
            cleaned_str = re.sub(r"\s+", " ", data).strip()

            try:
                # Check the maximum length
                if len(cleaned_str) > 90:
                    raise ValueError("The max length is 90 characters.")

                if len(cleaned_str) < 5:
                    raise ValueError("The minimum length is 5 characters")

                # Check data has letters and optional max 2 digit nr
                pattern = re.compile(
                    r"(?:[a-zA-Z0-9\s.,!-]*[a-zA-Z]+\s*\d{0,2}\s*"
                    r"[a-zA-Z0-9\s.,!-]*)+"
                )
                if bool(pattern.search(cleaned_str)) is False:
                    raise ValueError("Format incorrect.")
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
                return False
            return True

    def validate_is_date(self, date_str) -> bool:
        # first validate input is not empty
        if self.validate_not_empty(date_str):
            # strip trailing whitespaces and check format is correct
            date_str = date_str.strip()
            pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
            if pattern.match(date_str):
                date_format = "%Y-%m-%d"
                # check if it can be parsed to a date object
                try:
                    date_to_check = datetime.strptime(date_str, date_format)
                    current_date = datetime.now()
                    if date_to_check <= current_date:
                        return True
                    else:
                        print("Date cannot be greater than current date.")
                        return False
                except ValueError:
                    print("Date provided does not exist. Please try again.")
                    return False
            else:
                print("Invalid format. Should be YYYY-MM-DD")
                return False

    def validate_order_nr(self, data) -> bool:
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
                print(f"Invalid: {e} Please try again.\n")
                return False
            return True
