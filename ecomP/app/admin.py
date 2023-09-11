from django.contrib import admin
from . models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'selling_price', 'view_count')
    list_per_page = 5
    list_editable = ['selling_price']


admin.site.register(Product, ProductAdmin)
admin.site.register([Customer, Order, Cart, CartItem, Category,])
