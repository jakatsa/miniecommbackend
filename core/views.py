from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView
from .models import (
    User, Vendor, Category, Product, Order, OrderItem, Cart, CartItem,
    Shipping, Payment, Coupon, Review, WishList, Notification, Blog, 
    Contact, FAQ, Analytics, Configuration, Tax, Subscription, Refund
)
from .serializers import (
    UserSerializer,UserRegistrationSerializer, VendorSerializer, CategorySerializer, ProductSerializer, 
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

#refresh token cookies        
# class CustomRefreshToken(TokenRefreshView):
    def post (self,request ,*args,**kwargs):
        try:
            refresh_token=request.COOKIES.get('refresh_token')
            request.data['refresh']=refresh_token
            response=super().post(request,*args,**kwargs)

            tokens=response.data
            access_token=tokens['access']

            res=Response()
            res.data={'refreshed':True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'

            )
            return res

        except:     
            return Response({'refreshed':False})



# #access token cookies 
# class CustomTokenObtainPairView(TokenObtainPairView):
    def post (self,request ,*args,**kwargs):
        try:
            response=super().post(request,*args,**kwargs)
            tokens=response.data

            access_token=tokens['access']
            refresh_token=tokens['refresh']

            res=Response()
            res.data={'success':True}

            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res

        except:
            return Response({'success':False})    

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VendorViewSet(BaseViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer 

class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    


# View for anyone to get products
@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access explicitly
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# View for authenticated users to post products
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Enforce authentication
def post_products(request):
    user = request.user
    products = Product.objects.filter(vendor=user)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# def logout(request):
    try:
        res=Response()
        res.data={"success":True}
        res.delete_cookie('access_token',path='/',samesite='None')  
        res.delete_cookie('refresh_token',path='/',samesite='None')    
        return res
    except:
        return Response({"success":False})


# @api_view(['POST'])
# @permission_classes([AllowAny]) 
# def user_registration(request):
#     serializer=UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)    

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def is_Authenticated(request):
#     return Response({'authenticated':True})



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
