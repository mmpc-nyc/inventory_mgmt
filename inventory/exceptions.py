from django.core.exceptions import ValidationError


class ProductStatusError(ValidationError):
    """Exceptions related to Material Status"""
    ...


class MaterialConditionError(ValidationError):
    """Exceptions related to Material Condition"""
    ...


class StockLocationLogicError(ValidationError):
    """An error of logic"""
    ...


class MaterialOrderAssignmentError(ValidationError):
    """Material order assignment error"""


class OrderCompletionError(ValidationError):
    """A error occurred during the order completion process"""


class TransactionError(ValidationError):
    """An error occurred during a transaction process"""


class UserAuthorizationError(ValidationError):
    """An error when a user is not authorized"""
