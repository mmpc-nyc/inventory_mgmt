from main.exceptions import BaseError


class ItemStatusError(BaseError):
    """Exceptions related to Item Status"""
    pass


class ItemConditionError(BaseError):
    """Exceptions related to Item Condition"""
    pass


class InventoryLogicError(BaseError):
    """An error of logic"""
    pass