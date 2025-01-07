from rest_framework import serializers
from .models import (
    User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem,
    Shipping, Payment, Coupon, Review, WishList, Notification, Blog,
    Contact, FAQ, Analytics, Configuration, Tax, Subscription, Refund
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'    

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        return obj.parent.id if obj.parent else None

    class Meta:
        model = Category
        fields = '__all__'  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = OrderItemSerializer(many=True)  # Rename to match related_name

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_price = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            total_price += product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        order.total_price = total_price
        order.save()
        return order
        
class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Assuming Cart has multiple products
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__' 

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__' 

class ShippingSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = '__all__'   

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'                 

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'  

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'  

class WishListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Assuming multiple products
    customer = UserSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = '__all__'  

class NotificationSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'                        

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__' 

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'                         

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'   

class AnalyticsSerializer(serializers.ModelSerializer):
    popular_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Analytics
        fields = '__all__'    

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'   

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'  

class RefundSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Refund
        fields = '__all__' 
