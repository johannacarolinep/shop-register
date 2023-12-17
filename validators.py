def validate_quantity(data):
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
