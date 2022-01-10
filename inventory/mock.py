from django.contrib.auth import get_user_model

from inventory.models import Condition, Equipment
from inventory.models.product import Product
from inventory.models.stock import Stock

User = get_user_model()
users = [None]
for user in User.objects.all()[:2]:
    users.append(user)
stock = Stock.objects.all()[0]
product = Product.objects.all()[0]


def main():
    for condition in Condition.objects.all():
        for status, status_name in Equipment.Status.choices:
            for employee in users:
                Equipment.objects.create(
                    condition=condition,
                    status=status,
                    employee=employee,
                    product=product,
                    name=f'{product.name} {condition} {status_name} {employee or "No Employee"}')


if __name__ == '__main__':
    main()
