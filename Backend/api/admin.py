from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Address,
    StoreAdmin,
    Product,
    Store,
    Supplier,
    Inventory,
    Sales,
    SalesItems,
    InventoryMovement,
)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "city", "area", "created_at")
    list_filter = ("country", "city", "created_at")
    search_fields = ("country", "city", "area")
    ordering = ("country", "city", "area")
    fieldsets = (("Address Details", {"fields": ("country", "city", "area")}),)
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("country", "city", "area")}),
    )


@admin.register(StoreAdmin)
class StoreAdminAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )
    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username", "date_joined")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "cost_price",
        "sale_price",
        "discount",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("product_name", "description")
    ordering = ("product_name", "created_at")
    fieldsets = (
        ("Product Details", {"fields": ("product_name", "description")}),
        ("Pricing", {"fields": ("cost_price", "sale_price", "discount")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "product_name",
                    "description",
                    "cost_price",
                    "sale_price",
                    "discount",
                ),
            },
        ),
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "admin", "address", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name",)
    ordering = ("name", "created_at")
    fieldsets = (("Store Details", {"fields": ("name", "admin", "address")}),)
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("name", "admin", "address")}),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "contact_no", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "contact_no")
    ordering = ("name", "created_at")
    fieldsets = (("Supplier Details", {"fields": ("name", "contact_no")}),)
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("name", "contact")}),)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "store",
        "product",
        "quantity",
        "supplier",
        "reorder_level",
        "created_at",
    )
    list_filter = ("store", "supplier", "created_at")
    search_fields = ("store__name", "product__product_name", "supplier__name")
    ordering = ("store", "product", "created_at")
    fieldsets = (
        ("Inventory Details", {"fields": ("store", "product", "quantity", "supplier")}),
        ("Inventory Settings", {"fields": ("reorder_level", "last_restock_date")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "store",
                    "product",
                    "quantity",
                    "supplier",
                    "reorder_level",
                    "last_restock_date",
                ),
            },
        ),
    )


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "store",
        "total_quantity",
        "total_price",
        "overall_discount",
        "created_at",
    )
    list_filter = ("store", "created_at")
    search_fields = ("store__name", "id")
    ordering = ("-created_at",)
    fieldsets = (
        ("Sale Details", {"fields": ("store",)}),
        (
            "Sale Summary",
            {
                "fields": (
                    "total_quantity",
                    "total_tax",
                    "total_price",
                    "overall_discount",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "store",
                    "total_quantity",
                    "total_tax",
                    "total_price",
                    "overall_discount",
                ),
            },
        ),
    )


@admin.register(SalesItems)
class SalesItemsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sales",
        "product",
        "quantity",
        "unit_price",
        "discount",
        "created_at",
    )
    list_filter = ("sales__store", "created_at")
    search_fields = ("sales__id", "product__product_name")
    ordering = ("-created_at",)
    fieldsets = (
        ("Sale Item Details", {"fields": ("sales", "product", "quantity")}),
        ("Pricing", {"fields": ("unit_price", "discount")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "sales",
                    "product",
                    "quantity",
                    "unit_price",
                    "discount",
                ),
            },
        ),
    )


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "inventory",
        "quantity",
        "movement_type",
        "created_by",
        "created_at",
    )
    list_filter = ("movement_type", "created_at", "inventory__store")
    search_fields = ("inventory__product__product_name", "notes")
    ordering = ("-created_at",)
    fieldsets = (
        ("Movement Details", {"fields": ("inventory", "quantity", "movement_type")}),
        ("Transfer Information", {"fields": ("source_store", "destination_store")}),
        ("Additional Info", {"fields": ("created_by", "notes")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "inventory",
                    "quantity",
                    "movement_type",
                    "source_store",
                    "destination_store",
                    "created_by",
                    "notes",
                ),
            },
        ),
    )
