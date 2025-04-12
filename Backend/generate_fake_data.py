import random
from faker import Faker
from api.models import (
    Store,
    Product,
    Inventory,
    Supplier,
    StoreAdmin,
    Sales,
    SalesItems,
    Address,
)
from django.contrib.auth.models import User

fake = Faker()


# Create Fake Users for Store Admins
def create_users():
    for _ in range(10):  # Create 10 users
        user = StoreAdmin.objects.create_user(
            username=fake.user_name(), email=fake.email(), password="123"
        )
        user.save()


def create_address():
    for _ in range(20):
        Address.objects.create(
            country=fake.country(), city=fake.city(), area=fake.address()
        )


# Create Fake Stores
def create_stores():
    addresses = list(Address.objects.all())
    for _ in range(5):  # Create 5 stores
        store_admin = random.choice(
            StoreAdmin.objects.all()
        )  # Randomly assign store admins
        store = Store.objects.create(
            name=fake.company(),
            admin=store_admin,
            address=random.choice(addresses),
        )
        store.save()


# Create Fake Products
def create_products():
    for _ in range(20):  # Create 20 products
        product = Product.objects.create(
            product_name=fake.word(),
            description=fake.text(),
            cost_price=random.randint(10, 100),
            sale_price=random.randint(100, 500),
            discount=random.randint(5, 50),
        )
        product.save()


# Create Fake Suppliers
def create_suppliers():
    created_numbers = set()

    while len(created_numbers) < 5:
        number = fake.unique.msisdn()[:15]  # Generate a 15-digit phone number
        if number not in created_numbers:
            supplier = Supplier.objects.create(
                name=fake.company(),
                contact_no=number,
            )
            created_numbers.add(number)


# Create Fake Inventory Data
def create_inventory():
    for _ in range(50):  # Create 50 inventory records
        store = random.choice(Store.objects.all())
        product = random.choice(Product.objects.all())
        supplier = random.choice(Supplier.objects.all())
        inventory = Inventory.objects.create(
            store=store,
            product=product,
            quantity=random.randint(1, 100),
            supplier=supplier,
            reorder_level=random.randint(10, 50),
            last_restock_date=fake.date_this_year(),
        )
        inventory.save()


def create_fake_sales(num_sales=50):
    stores = Store.objects.all()
    products = list(Product.objects.all())

    for _ in range(num_sales):
        store = random.choice(stores)
        total_price = 0
        sale = Sales.objects.create(
            store=store,
        )

        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            price = float(product.sale_price)
            total_price += price * quantity

            SalesItems.objects.create(
                sales=sale, product=product, quantity=quantity, unit_price=price
            )

        sale.total_price = total_price
        sale.save()


# Call functions to populate data
# create_users()
# create_address()
# create_stores()
# create_products()
# create_suppliers()
# create_inventory()
create_fake_sales()
print("Fake data has been generated and inserted into the database.")
