class BaseError(Exception):
    """Exceptions related to inventory"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}'


class JobStatusError(BaseError):
    """Error related to job status"""
    pass


