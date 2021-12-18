from inventory.models import Inventory, Product, ProductType
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.all()[0]
inventory = Inventory.objects.all()[0]


def main():
    product_id = 0
    for i in range(100):
        product_type = ProductType.objects.create(name=f'Product Type {i}', short_name=f'product_type_{i}')
        for j in range(100):
            Product.objects.create(name=f'Product {product_id}', product_type=product_type, created=user)
            product_id += 1


if __name__ == '__main__':
    main()