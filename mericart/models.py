from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=15)
    phone_number = models.IntegerField('Mobile Number')
    address = models.TextField('Address')
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    pin_code = models.IntegerField('Pin_Code')
    
    def __str__(self):
        return self.user.username   

class Category(models.Model):
    category_name = models.CharField(max_length=25)
    category_code = models.CharField(max_length=25)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand = models.CharField(max_length = 25)
    description = models.TextField('Description')

    def __str__(self):
        return self.brand



class Product(models.Model):
    photo = models.ImageField(upload_to='Products/', default='Products/no_item.gif')
    name = models.CharField(max_length=25)
    product_code = models.CharField(max_length = 25)
    price = models.FloatField(default = 0.0)
    discount = models.IntegerField(default = 0)    
    description = models.TextField(default = "No Product Details" )
    category = models.ForeignKey(Category)
    added_date = models.DateTimeField(auto_now_add = True)
    brand = models.ForeignKey(Brand)
    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.OneToOneField(Product)
    stock_no = models.IntegerField(default = 0)
    stock_last_updated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.name

class Cart(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    total_no_product = models.IntegerField(default = 1)
    total_cost = models.FloatField(default = 0)
    cart_added = models.DateTimeField(auto_now_add = True)
    purchased = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username  

class Shipping(models.Model):
    user = models.OneToOneField(User)
    street_add = models.TextField(blank = True)
    land_mark = models.CharField(max_length = 50,blank = True)
    country = models.CharField(max_length = 30,blank = True)
    state = models.CharField(max_length = 30,blank = True)
    city = models.CharField(max_length = 30,blank = True)
    postel_pin = models.IntegerField(blank = True)
    mobile_no = models.IntegerField(blank = True)
    alternative_no = models.IntegerField(blank = True)
    
    def __str__(self):
        return self.user.username

class Pay(models.Model):
    order_no = models.CharField(max_length = 50)
    payment_type = models.CharField(max_length = 50)
    card_no = models.CharField(max_length = 18, blank = True)
    cvv = models.IntegerField(default = 0)
    expiry = models.CharField(max_length = 10, blank = True)

    def __str__(self):
        return self.payment_type

class Billing(models.Model):
    user = models.ForeignKey(User)
    order_no = models.CharField(max_length = 50)
    product_name = models.CharField(max_length = 50)
    product_code = models.CharField(max_length = 50)
    quantity = models.IntegerField()
    single_price = models.FloatField()
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add = True)
    shipping_address = models.TextField()
    pay = models.ForeignKey(Pay)
    status = models.CharField(max_length = 50)

    def __str__(self):
        return self.order_no

