def validate_quantity(data) -> bool:
    """
    Validates data, returns true if data is a positive integer value.
    """
    try:
        # checks if empty
        if not data:
            raise ValueError("Data cannot be empty. Please try again.")
        # tries to convert to int
        quantity = int(data)

        # checks if <= 0
        if quantity <= 0:
            raise ValueError(
                "Quantity must be a positive integer value. Please try again"
            )
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            print(
                "Invalid input. Quantity must be a positive integer. Please try again"
            )
        else:
            print(f"Invalid: {e} Please try again.\n")

        return False

    return True


def validate_article_nr(data) -> bool:
    """
    Validates data, returns true if data is a positive 4 digit integer value.
    """
    try:
        # checks if empty
        if not data:
            raise ValueError("Data cannot be empty. Please try again.")
        # tries to convert to int
        article_nr = int(data)

        # checks if outside of scope for art. numbers
        if article_nr > 9999 or article_nr < 1000:
            raise ValueError("Must be a positive 4 digit integer. Try again")
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            print(
                "Invalid input. Quantity must be a positive integer. Please try again"
            )
        else:
            print(f"Invalid: {e} Please try again.\n")

        return False

    return True
