from django.urls import path
from api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", ProductViewsSet)
router.register("sales", SalesViewsSet)
router.register("inventory", InventoryViewsSet)
router.register("store-admin", StoreAdminViewsSet)
router.register("supplier", SupplierViewsSet)
router.register("address", AddressViewsSet)
router.register("store", StoreViewsSet)
urlpatterns = []
urlpatterns += router.urls
