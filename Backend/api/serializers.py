from rest_framework import serializers
from .models import *
from decimal import Decimal
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["product_name", "cost_price", "sale_price", "discount", "description"]


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ["country", "city", "area"]


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ["name", "contact"]


class StoreAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAdmin
        fields = ["username", "email"]


class StoreSerializer(serializers.ModelSerializer):
    store_admin = StoreAdminSerializer(read_only=True)
    store_admin_id = serializers.PrimaryKeyRelatedField(
        queryset=StoreAdmin.objects.all(), write_only=True, source="store_admin"
    )

    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), write_only=True, source="address"
    )

    class Meta:
        model = Store
        fields = ["name", "store_admin", "store_admin_id", "address", "address_id"]


class InventoryReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "store",
            "product",
            "quantity",
            "supplier",
            "reorder_level",
            "last_restock_date",
            "created_at",
        ]


# For create/update
class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class SalesItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = SalesItems
        fields = ["product", "quantity", "unit_price", "discount", "created_at"]


class SalesReadSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class SalesItemsCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = SalesItems
            fields = ["product", "quantity", "unit_price", "discount", "created_at"]

    sales_item = SalesItemsSerializer(read_only=True, many=True)

    class Meta:
        model = Sales
        fields = [
            "store",
            "sales_item",
            "total_quantity",
            "total_tax",
            "total_price",
            "overall_discount",
            "grand_total",
            "created_at",
        ]


class SalesCreateSerilaizer(serializers.ModelSerializer):
    sales_item = SalesItemsSerializer(many=True)

    class Meta:
        model = Sales
        fields = [
            "id",
            "store",
            "sales_item",
            "created_at",
            "total_quantity",
            "total_price",
            "total_tax",
            "overall_discount",
            "grand_total",
        ]

        read_only_fields = [
            "total_quantity",
            "total_price",
            "total_tax",
            "overall_discount",
            "grand_total",
        ]

    # PAYLOAD
    # {
    #     store:1,
    #     sales_items:[
    #         {
    #             product:1,
    #             quantity:4,
    #         },
    #         {
    #             product:3,
    #             quantity:5,
    #         }
    #     ]
    #     discount:20
    # }

    def create(self, validated_data):
        sales_items_data = validated_data.pop("sales_item")
        store = validated_data.pop("store", None)

        if not store:
            raise serializers.ValidationError("Store is required.")

        with transaction.atomic():
            total_quantity = 0
            total_price = Decimal("0.00")

            sales = Sales.objects.create(store=store, **validated_data)

            for item in sales_items_data:
                product = item["product"]
                quantity = item["quantity"]

                total_quantity += quantity
                effective_price = product.sale_price - (
                    product.sale_price * (product.discount / Decimal("100"))
                )
                subtotal = effective_price * quantity
                total_price += subtotal

                SalesItems.objects.create(
                    sales=sales,
                    product=product,
                    quantity=quantity,
                    unit_price=product.sale_price,
                    discount=product.discount,
                )

            discount_percent = validated_data.get("overall_discount", Decimal("0"))
            total_tax = Decimal("0.10") * total_price  # 10% tax

            sales.total_quantity = total_quantity
            sales.total_price = total_price
            sales.total_tax = total_tax
            sales.overall_discount = discount_percent
            sales.save()

        return sales

    def update(self, instance, validated_data):
        sales_items_data = validated_data.pop("sales_item", [])
        discount = validated_data.pop("overall_discount", instance.overall_discount)

        total_quantity = 0
        total_price = 0

        with transaction.atomic():
            # Delete old sales items
            instance.sales_item.all().delete()

            for item in sales_items_data:
                product = Product.objects.get(id=item["product"].id)
                quantity = item["quantity"]
                unit_price = product.sale_price
                product_discount = product.discount

                total_quantity += quantity
                item_price = quantity * (
                    unit_price - (unit_price * product_discount / 100)
                )
                total_price += item_price

                SalesItems.objects.create(
                    sales=instance,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    discount=product_discount,
                )

            total_tax = total_price * 0.10
            grand_total = total_price + total_tax - (total_price * (discount / 100))

            # Update the instance fields
            instance.total_quantity = total_quantity
            instance.total_price = total_price
            instance.total_tax = total_tax
            instance.overall_discount = discount
            instance.save()

        return instance
