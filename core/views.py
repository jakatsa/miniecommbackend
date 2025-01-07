from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import (
    User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem,
    Shipping, Payment, Coupon, Review, WishList, Notification, Blog, 
    Contact, FAQ, Analytics, Configuration, Tax, Subscription, Refund
)
from .serializers import (
    UserSerializer, VendorSerializer, CategorySerializer, ProductSerializer, 
    OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer,
    ShippingSerializer, PaymentSerializer, CouponSerializer, ReviewSerializer, 
    WishListSerializer, NotificationSerializer, BlogSerializer, ContactSerializer, 
    FAQSerializer, AnalyticsSerializer, ConfigurationSerializer, 
    TaxSerializer, SubscriptionSerializer, RefundSerializer
)

class BaseViewSet(viewsets.ModelViewSet):
    """A base viewset that provides default behaviors for all viewsets."""
    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VendorViewSet(BaseViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer 

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
class CartViewSet(BaseViewSet):
    queryset = Cart.objects.all()  # Corrected here
    serializer_class = CartSerializer  

class CartItemViewSet(BaseViewSet):
    queryset = CartItem.objects.all()  # Corrected here
    serializer_class = CartItemSerializer    

class ShippingViewSet(BaseViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer     

class PaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer  

class CouponViewSet(BaseViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer          

class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer 

class WishListViewSet(BaseViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer   

class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer    

class BlogViewSet(BaseViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer      

class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer     

class FAQViewSet(BaseViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer  

class AnalyticsViewSet(BaseViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer     

class ConfigurationViewSet(BaseViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer    

class TaxViewSet(BaseViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer        

class SubscriptionViewSet(BaseViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer    

class RefundViewSet(BaseViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer              
