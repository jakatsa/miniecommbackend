
from django.db import models
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    is_vendor = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    

class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")
    bio = models.TextField()
    contact_details=models.TextField()
    bank_details = models.TextField()
    shipping_policy=models.TextField()   
    return_policy=models.TextField() 

class Category(models.Model):
    name=models.CharField(max_length =100)
    slug = models.SlugField(max_length=100,unique=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE , null =True,blank=True,related_name="subcategory")

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    slug=models.SlugField(max_length=100,unique=True)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price=models.DecimalField( max_digits=5, decimal_places=2)
    discount_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    stock=models.IntegerField()
    #available=models.BooleanField(default=True)
    images=models.ImageField(upload_to='products/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #sku =models.CharField(max_length=100,unique=True)
    #rating = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    #status = models.CharField(max_length=50,choices=[
    #    ('pending','Pending'),
    #    ('completed','Completed'),
    #    ('canceled','Canceled'),
    #    ('shipped','Shipped'),
    #    ('delivered','Deleivered'),
    #])        
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    #order_date=models.DateTimeField(auto_now_add=True)
    shipping_address =models.TextField()
    #billing_address= models.TextField(blank=True,null=True)
    products =models.ManyToManyField(Product,through='OrderItem')#Items Ordered:You can use a Many-to-Many relationship with a Product model if you expect orders to contain multiple products.
    #quantity=models.PositiveIntegerField(default=1)
    #payment_method=models.CharField(max_length=50,choices=[
    #    ('credit_card','credit Card'),
    #    ('paypal','PayPal'),
    #    ('bank_transfer','Bank Transfer')
    #    ('mpesa', 'Mpesa')
    #])
    #transaction_id= models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True )
    def __str__(self):
        return f'Order {self.id} by {self.customer.name}'
          
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'  

class Cart(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product =models.ManyToManyField(Product,through='CartItem')
    session_key = models.CharField(max_length=40, null=True, blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True )

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price =  models.DecimalField(max_digits=10,decimal_places=2)

class Shipping(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100)#name of shipping 
    description=models.TextField()
    rate=models.DecimalField(max_digits=10,decimal_places=2)

    #address=models.CharField(max_length=100)
    #county=models.CharField(max_length=100)
    #country=models.CharField(max_length=100)
    #shipping_method=models.CharField(max_length=100,choices=[
     #   ('standard', 'Standard'),
     #   ('express', 'Express'), 
     #   ('overnight', 'Overnight')
    #])
    
    #shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    #estimated_delivery = models.DateField()
    #tracking_number = models.CharField(max_length=100, null=True, blank=True)
    #status = models.CharField(max_length=50, choices=[
     #   ('pending', 'Pending'), 
     #   ('shipped', 'Shipped'), 
     #   ('delivered', 'Delivered')
     #   ])
    #order = models.OneToOneField(Order, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payment')
    payment_method=models.CharField(max_length=50,choices=[
        ('credit_card','credit Card'),
        ('paypal','PayPal'),
        ('bank_transfer','Bank Transfer'),
        ('mpesa', 'Mpesa')
    ])
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True) 

class Coupon (models.Model):
    code = models.CharField(max_length=100,unique=True)
    discount = models.DecimalField(max_digits=  10,decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    rating= models.PositiveIntegerField()
    comment= models.TextField()
    created_at=models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class WishList(models.Model):
    customer= models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    products= models.ManyToManyField(Product,related_name="wishlist")

class Notification(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField(max_length=200,unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    slug = models.SlugField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()   
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question =models.TextField()
    answer = models.TextField()   

class Analytics(models.Model):
    sales=models.DecimalField(max_digits=10,decimal_places=2)
    traffic=models.PositiveIntegerField()
    popular_products=models.ManyToManyField(Product,related_name='analytics')
    created_at = models.DateTimeField(auto_now_add=True)

class Configuration(models.Model):
    site_name=models.CharField(max_length=100)
    site_description=models.TextField()
    site_logo=models.ImageField(upload_to='logos')

class Tax(models.Model):
    name=models.CharField(max_length=100)
    rate=models.DecimalField(max_digits=5,decimal_places=2)
    country=models.CharField(max_length=100)
    county= models.CharField(max_length=100,null=True,blank=True)

class Subscription(models.Model):
    email=models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='refunds')
    reason=models.TextField
    amount=models.DecimalField(max_digits=5,decimal_places=2)
    status = models.CharField(max_length=50,choices=[
        ('pending','Pending'),
        ('completed','Completed'),
        ('canceled','Canceled'),
        ('shipped','Shipped'),
        ('delivered','Deleivered'),
    ])  
    requested_at =models.DateTimeField(auto_now_add=True)
    processed_at =models.DateTimeField(null=True,blank=True)







        






    


