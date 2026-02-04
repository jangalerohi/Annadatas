from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class SliderModel(models.Model):
    slider_title = models.CharField(max_length=250)
    slider_description = models.TextField()
    slider_image = models.ImageField(upload_to='static/img/')
    slider_btn_title = models.CharField(max_length=100)
    slider_btn_link = models.CharField(max_length=100)
    
    
class FeaturesModel(models.Model):
    section_title = models.CharField(max_length=250)
    feature_icon = models.CharField(max_length=250)
    feature_title = models.CharField(max_length=250)
    feature_description = models.TextField()
    
class productsmodel(models.Model):
    product_name = models.CharField(max_length=250)
    product_image = models.ImageField(upload_to='static/img/')
    product_weight=models.CharField(max_length=50)
    product_price=models.CharField(max_length=250)
    product_add_to_cart=models.CharField(max_length=250)
     
    def __str__(self):
        return self.product_name
class AboutSectionhomeModel(models.Model):
    about_title = models.CharField(max_length=250)
    about_description = models.TextField()
    about_image = models.ImageField(upload_to='static/img/')
    about_btn_title = models.CharField(max_length=100)
    about_btn_link = models.CharField(max_length=100)

    def __str__(self):
        return self.about_title
class TestimonialsModel(models.Model):
    Testimonials_star = models.CharField(max_length=250)
    Testimonials_description=models.TextField()
    Testimonials_name_address=models.CharField(max_length=250)

class ProductsHeroModel(models.Model):
    hero_title = models.CharField(max_length=200)
    hero_description = models.TextField()
    hero_image = models.ImageField(upload_to='static/img/')

    def __str__(self):
        return self.hero_title
class Product(models.Model):
    name = models.CharField(max_length=200)                     # Toor Dal
    title = models.CharField(max_length=250)                    # Toor Dal (अरहर दाल)
    weight = models.CharField(max_length=100)                   # 500gm Pack
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/img/')           # img/Toor_Dal.jpg
    details_image = models.URLField(blank=True, null=True)      # unsplash link
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=250)  # No login needed

    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"
    


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_METHOD = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cod')
    
    # Razorpay fields जोडा
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    
    
  



    
    
    
    
    
    
    
  

   
