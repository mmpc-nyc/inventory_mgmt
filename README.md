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
def pickup(Equipment, User):
    is_authenticated(User)
    is_authorized(User)
    check_condition(Equipment)
    
    
    check_product_status(Product)
    check_generic_product_status(GenericProduct)
    
    Equipment.User = User
    Equipment.Status = EquipmentStatus.PICKED_UP
    Equipment.save()
```