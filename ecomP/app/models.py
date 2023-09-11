from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.title

class Product(models.Model):
    product_title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500)
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    product_photo = models.ImageField(upload_to = 'products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    def __str__(self)->str:
        return self.product_title

    class Meta:
        ordering = ['product_title']

class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['joined_on']

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart_id) + "CartItem: " + str(self.id)

ORDER_STATUS = [
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
]

class Order(models.Model):
    
    placed_at = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE) 
    ordered_by = models.CharField(max_length=200)
    order_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=60, choices = ORDER_STATUS)
    
    def __str__(self):
        return "Order: " + str(self.id)