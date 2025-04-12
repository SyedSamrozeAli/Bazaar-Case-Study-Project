import django_filters
from .models import Product, Sales, Inventory, Address, StoreAdmin, Store, Supplier


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "product_name": ["iexact", "icontains"],
            "cost_price": ["exact", "lte", "gte", "range"],
            "sale_price": ["exact", "lte", "gte", "range"],
            "discount": ["exact", "lte", "gte", "range"],
            "created_at": ["exact", "lte", "gte", "range"],
            "updated_at": ["exact", "lte", "gte", "range"],
            "description": ["iexact", "icontains"],
        }


class SalesFilter(django_filters.FilterSet):
    class Meta:
        model = Sales
        fields = {
            "store__name": ["iexact", "icontains"],
            "total_quantity": ["exact", "lte", "gte", "range"],
            "total_tax": ["exact", "lte", "gte", "range"],
            "total_price": ["exact", "lte", "gte", "range"],
            "overall_discount": ["exact", "lte", "gte", "range"],
            "created_at": ["exact", "lte", "gte", "range"],
            "updated_at": ["exact", "lte", "gte", "range"],
        }


class InventoryFilters(django_filters.FilterSet):
    class Meta:
        model = Inventory
        fields = {
            "store__name": ["iexact", "icontains"],
            "supplier__name": ["iexact", "icontains"],
            "product__product_name": ["iexact", "icontains"],
            "quantity": ["exact", "lte", "gte", "range"],
            "reorder_level": ["exact", "lte", "gte", "range"],
            "last_restock_date": ["exact", "lte", "gte", "range"],
            "created_at": ["exact", "lte", "gte", "range"],
            "updated_at": ["exact", "lte", "gte", "range"],
        }


class AddressFilters(django_filters.FilterSet):
    class Meta:
        model = Address
        fields = {
            "country": ["iexact", "icontains"],
            "city": ["iexact", "icontains"],
            "area": ["iexact", "icontains"],
        }


class StoreAdminFilters(django_filters.FilterSet):
    class Meta:
        model = StoreAdmin
        fields = {
            "username": ["iexact", "icontains"],
            "first_name": ["iexact", "icontains"],
            "last_name": ["iexact", "icontains"],
            "email": ["iexact", "icontains"],
        }


class StoreFilters(django_filters.FilterSet):
    class Meta:
        model = Store
        fields = {
            "name": ["iexact", "icontains"],
            "admin__username": ["iexact", "icontains"],
            "created_at": ["exact", "lte", "gte", "range"],
        }


class SupplierFilters(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = {
            "name": ["iexact", "icontains"],
        }
