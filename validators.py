import re


class Validators:
    def validate_not_empty(self, data) -> bool:
        """
        Validates data, returns true if data exists.
        """
        try:
            if not data:
                raise ValueError("Data cannot be empty. Please try again.")
        except ValueError as e:
            print(f"Invalid: {e} Please try again.\n")
            return False
        return True

    def validate_is_positive(self, data) -> bool:
        try:
            temp_int = int(data)
            if temp_int <= 0:
                raise ValueError("Data must be a positive value. Please try again")
        except ValueError as e:
            print(f"Invalid: {e} Please try again.\n")
            return False
        return True

    def validate_is_int(self, data) -> bool:
        try:
            temp_int = int(data)
        except ValueError:
            print("Invalid input. Data must be an integer. " "Please try again")
            return False
        return True

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
                    raise ValueError("Must be a positive 4 digit integer. Try again")
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
                    raise ValueError("The max length for names is 90 characters.")

                if len(cleaned_str) < 5:
                    raise ValueError("The minimum length is 5 characters")

                # Use a regular expression to check for letters and optional max 2 digit nr
                pattern = re.compile(
                    r"(?:[a-zA-Z0-9\s.,!-]*[a-zA-Z]+\s*\d{0,2}\s*[a-zA-Z0-9\s.,!-]*)+"
                )
                if bool(pattern.search(cleaned_str)) is False:
                    raise ValueError("Format incorrect.")
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
                return False
            return True
