#Inventory Management for tracking Equpment

## Models

### Customer
### Order
### Location
### Stock
### Generic Product
### Product
### Equipment
### Transaction

## Actions
### Pickup
```
Class Order:


Class Equipment:
    def pickup(User):
        is_authenticated(User)
        is_authorized(User)
        
        check_product_status(Product)
        check_generic_product_status(GenericProduct)
        
        Equipment.User = User
        Equipment.Status = EquipmentStatus.PICKED_UP
        Equipment.save()
        
    def deploy():
        is_authenticated(User)
        is_authorized(User)
        
    def store():
        is_authenticated(User)
        is_authorized(User)
        is_storable(Condition)
```