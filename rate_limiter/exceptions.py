class RateLimitExceeded(Exception):
    """Raised when an entity exceeds the allowed request limit."""

    def __init__(self, message="Request limit exceeded. Please try again later."):
        super().__init__(message)
