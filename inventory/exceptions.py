from main.exceptions import BaseError


class ProductStatusError(BaseError):
    """Exceptions related to Product Status"""
    ...


class ProductConditionError(BaseError):
    """Exceptions related to Product Condition"""
    ...


class StockLogicError(BaseError):
    """An error of logic"""
    ...
