from django.db import models
from django.db.models import Q, F, Func
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Length


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "city", "area"], name="unique_address"
            )
        ]

    def __str__(self):
        return f"{self.country}, {self.city}, {self.area}"


class StoreAdmin(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group", related_name="store_admin_users", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="store_admin_users", blank=True
    )

    def __str__(self):
        return self.username


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product_name"]),  # For product searches
            models.Index(fields=["created_at"]),  # For date filtering
        ]
        constraints = [
            models.CheckConstraint(name="check_cost_price", check=Q(cost_price__gte=0)),
            models.CheckConstraint(name="check_sale_price", check=Q(sale_price__gte=0)),
            models.CheckConstraint(
                name="check_product_discount", check=Q(discount__gte=0)
            ),
        ]

    def __str__(self):
        return self.product_name


class Store(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    admin = models.OneToOneField(
        StoreAdmin, on_delete=models.CASCADE, related_name="store"
    )
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="store"
    )
    products = models.ManyToManyField(
        Product, through="Inventory", related_name="store"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),  # For store searches
            models.Index(fields=["address"]),  # For geographic lookups
        ]

    def __str__(self):
        return f"{self.name}-{self.admin.username}"


class Supplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),  # For supplier searches
        ]

    def __str__(self):
        return self.name


class Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventory")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="inventory"
    )
    reorder_level = models.PositiveIntegerField(default=10)
    last_restock_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["store", "product", "supplier"],
                name="unique_store_product_supplier",
            )
        ]
        indexes = [
            models.Index(fields=["store", "product"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.store.name}-{self.product.product_name}"


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="sales")
    total_quantity = models.PositiveIntegerField(default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overall_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products = models.ManyToManyField(
        Product, through="SalesItems", related_name="sales"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def grand_total(self):
        return (
            self.total_price
            + (self.total_price * (self.total_tax / 100))
            - self.total_price * (self.overall_discount / 100)
        )

    def __str__(self):
        return f"Sales {self.id} by {self.store.admin.username}"

    class Meta:
        indexes = [
            models.Index(fields=["store"]),  # For store-specific queries
            models.Index(fields=["created_at"]),  # For date range reporting
        ]
        constraints = [
            models.CheckConstraint(name="check_total_tax", check=Q(total_tax__gte=0)),
            models.CheckConstraint(
                name="check_sales_total_discount", check=Q(overall_discount__gte=0)
            ),
            models.CheckConstraint(
                name="check_sales_total_price", check=Q(total_price__gte=0)
            ),
        ]


class SalesItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(
        Sales, on_delete=models.CASCADE, related_name="sales_item"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sales_item"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item_subtotal(self):
        return self.quantity * (
            self.unit_price - (self.unit_price * (self.discount / 100))
        )

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in SALE {self.sales.id}"

    class Meta:
        indexes = [
            models.Index(fields=["sales", "product"]),  # Common joined query
            models.Index(fields=["created_at"]),  # Time-based queries
        ]
        constraints = [
            models.CheckConstraint(name="check_unit_price", check=Q(unit_price__gte=0)),
            models.CheckConstraint(
                name="check_sales_discount", check=Q(discount__gte=0)
            ),
        ]


class InventoryMovement(models.Model):
    STOCK_IN = "STOCK_IN"
    SALE = "SALE"
    REMOVAL = "REMOVAL"
    ADJUSTMENT = "ADJUSTMENT"
    TRANSFER = "TRANSFER"

    MOVEMENT_TYPE_CHOICES = [
        (STOCK_IN, "Stock In"),
        (SALE, "Sale"),
        (REMOVAL, "Manual Removal"),
        (ADJUSTMENT, "Inventory Adjustment"),
        (TRANSFER, "Store Transfer"),
    ]

    id = models.BigAutoField(primary_key=True)
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="movements"
    )
    quantity = models.IntegerField()  # Can be negative for removals/sales
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    source_store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="outgoing_movements",
        null=True,
        blank=True,
    )
    destination_store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="incoming_movements",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(StoreAdmin, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["inventory"]),
        ]
