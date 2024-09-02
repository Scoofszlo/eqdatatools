class InvalidURLError(Exception):
    """Custom exception for invalid URLs."""

    def __init__(self, URL):
        self.message = f"The URL '{URL}' is not valid."
        super().__init__(self.message)

class InvalidDateFormat(Exception):
    """Custom exception for invalid date formats."""
    def __init__(self):
        self.message = "Invalid date format detected. Problem is most likely due to inconsistent HTML element structure."
        super().__init__(self.message)
