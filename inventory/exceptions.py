from django.core.exceptions import ValidationError


class ProductStatusError(ValidationError):
    """Exceptions related to Product Status"""
    ...


class ProductConditionError(ValidationError):
    """Exceptions related to Product Condition"""
    ...


class StockLogicError(ValidationError):
    """An error of logic"""
    ...


class ProductOrderAssignmentError(ValidationError):
    """Product order assignment error"""


class OrderCompletionError(ValidationError):
    """A error occurred during the order completion process"""


class TransactionError(ValidationError):
    """An error occurred during a transaction process"""
