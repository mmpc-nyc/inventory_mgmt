from main.exceptions import BaseError


class ProductStatusError(BaseError):
    """Exceptions related to Product Status"""
    pass


class ProductConditionError(BaseError):
    """Exceptions related to Product Condition"""
    pass


class InventoryLogicError(BaseError):
    """An error of logic"""
    pass