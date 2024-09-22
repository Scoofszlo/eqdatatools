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


class InvalidCoordinatesFormat(Exception):
    """Custom exception for invalid coordinate format."""

    def __init__(self, entry, pattern):
        self.message = f"Invalid coordinate format detected. Check if the pattern matches the source properly:\n\n\tentry: {entry}\n\tpattern: {pattern}"
        super().__init__(self.message)


class InvalidDepthFormat(Exception):
    """Custom exception for invalid depth format."""

    def __init__(self, entry, pattern):
        self.message = f"Invalid depth format detected. Check if the pattern matches the source properly\n\n\tentry: {entry}\n\tpattern: {pattern}"
        super().__init__(self.message)
