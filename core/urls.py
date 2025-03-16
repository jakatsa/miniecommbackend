from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, VendorViewSet, CategoryViewSet, ProductViewSet, OrderViewSet,
    OrderItemViewSet, CartViewSet, CartItemViewSet, ShippingViewSet, 
    PaymentViewSet, CouponViewSet, ReviewViewSet, WishListViewSet, 
    NotificationViewSet, BlogViewSet, ContactViewSet, FAQViewSet,
    AnalyticsViewSet, ConfigurationViewSet, TaxViewSet, SubscriptionViewSet, 
    RefundViewSet
)

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'shippings', ShippingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlists', WishListViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'configurations', ConfigurationViewSet)
router.register(r'tax', TaxViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'refunds', RefundViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
  
]
