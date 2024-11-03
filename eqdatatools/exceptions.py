class InvalidURLError(Exception):
    """Custom exception for invalid URLs."""

    def __init__(self, url: str) -> None:
        self.message = f"The URL '{url}' is not valid."
        super().__init__(self.message)


class InvalidDateFormat(Exception):
    """Custom exception for invalid date formats."""

    def __init__(self, datetime_str: str) -> None:
        self.message = f"The date format '{datetime_str}' is invalid."
        super().__init__(self.message)


class InvalidCoordinatesFormat(Exception):
    """Custom exception for invalid coordinate format."""

    def __init__(self, entry: str, pattern: str) -> None:
        self.message = f"Invalid coordinate format detected. Check if the pattern matches the source properly:\n\n\tentry: {entry}\n\tpattern: {pattern}"
        super().__init__(self.message)


class InvalidDepthFormat(Exception):
    """Custom exception for invalid depth format."""

    def __init__(self, entry: str, pattern: str) -> None:
        self.message = f"Invalid depth format detected. Check if the pattern matches the source properly\n\n\tentry: {entry}\n\tpattern: {pattern}"
        super().__init__(self.message)
