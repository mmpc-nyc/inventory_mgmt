from main.exceptions import BaseError


class InventoryItemStatusError(BaseError):
    """Exceptions related to InventoryItem Status"""
    pass


class InventoryItemConditionError(BaseError):
    """Exceptions related to InventoryItem Condition"""
    pass


class InventoryLogicError(BaseError):
    """An error of logic"""
    pass