from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from .filter import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class ProductViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    # Adding Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = "page_num"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    # Adding Filters
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "product_name",
        "cost_price",
        "sale_price",
        "discount",
        "created_at",
    ]

    def get_queryset(self):
        """
        A store admin will get to see only their products.
        """
        # # Check for cache first
        # cache_key = f"product_list_{self.request.user.id}"
        # cached_products = cache.get(cache_key)

        # if cached_products is not None:
        #     # Return cached products if available
        #     return cached_products

        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(inventory__store__admin=self.request.user).distinct()

        # Cache the queryset results for 10 minutes
        # cache.set(cache_key, qs, timeout=600)

        return qs

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single product and cache it.
        """
        # product_id = kwargs.get("pk")
        # cache_key = f"product_{product_id}"
        # cached_product = cache.get(cache_key)

        # if cached_product is not None:
        #     # Return cached product if available
        #     return Response(self.get_serializer(cached_product).data)

        # If product is not in cache, get it from the database
        # instance = self.get_object()
        # # Cache the product for 10 minutes
        # cache.set(cache_key, instance, timeout=600)

        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Override the default `perform_create` to invalidate cache when a new product is added.
        """
        instance = serializer.save()
        # Invalidate the product list cache when a new product is added
        # cache.delete(f"product_list_{self.request.user.id}")
        return instance

    def perform_update(self, serializer):
        """
        Override the default `perform_update` to invalidate cache when a product is updated.
        """
        instance = serializer.save()
        # Invalidate the product list and specific product cache when updated
        # cache.delete(f"product_list_{self.request.user.id}")
        # cache.delete(f"product_{instance.id}")
        return instance

    def perform_destroy(self, instance):
        """
        Override the default `perform_destroy` to invalidate cache when a product is deleted.
        """
        # Invalidate the product list cache when a product is deleted
        # cache.delete(f"product_list_{self.request.user.id}")
        # cache.delete(f"product_{instance.id}")
        instance.delete()


class SalesViewsSet(viewsets.ModelViewSet):
    queryset = Sales.objects.prefetch_related(
        "store", "store__address", "sales_item", "sales_item__product"
    )
    serializer_class = SalesReadSerializer
    permission_classes = [IsAuthenticated]
    # Adding Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = "page_num"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    # Adding Filters
    filterset_class = SalesFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "total_quantity",
        "total_price",
        "sale_tax",
        "total_discount",
        "grand_total",
        "created_at",
    ]

    # A store admin will get to see only his sales
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(store__admin=self.request.user)
        return qs

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST" or self.request.method == "PUT":
            return SalesCreateSerilaizer
        return super().get_serializer(*args, **kwargs)


class StoreViewsSet(viewsets.ModelViewSet):
    queryset = Store.objects.prefetch_related("admin")
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    # Adding Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = "page_num"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    # Adding Filters
    filterset_class = StoreFilters
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "name",
        "admin__username",
        "created_at",
    ]

    # A store admin will get to see only his store
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(admin=self.request.user)
        return qs


class SupplierViewsSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    # Adding Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = "page_num"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    # Adding Filters
    filterset_class = SupplierFilters
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name", "contact", "created_at"]

    # A store admin will get to see only his supplier
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(inventory__store__admin=self.request.user).distinct()
        return qs


class StoreAdminViewsSet(viewsets.ModelViewSet):
    queryset = StoreAdmin.objects.all()
    serializer_class = StoreAdminSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = StoreAdminFilters
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "created_at",
    ]

    # A store admin will get to see only his info
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(store__admin=self.request.user)
        return qs


class InventoryViewsSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.prefetch_related("store__admin", "product")
    serializer_class = InventoryReadSerializer
    permission_classes = [IsAuthenticated]

    # Adding Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = "page_num"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 10

    # A store admin will get to see only his inventory
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(store__admin=self.request.user)
        return qs

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST" or self.request.method == "PUT":
            return InventoryCreateSerializer
        return super().get_serializer(*args, **kwargs)


class AddressViewsSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    # A store admin will get to see only his address details
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            return qs.filter(store__admin=self.request.user)
        return qs
