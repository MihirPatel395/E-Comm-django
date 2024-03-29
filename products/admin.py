from django.contrib import admin
from .models import  *

# create modelAdmin
class OrderItemAdmin(admin.ModelAdmin):
    list_display=[
        'product',
        'order',
        'quantity'
    ]
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        'name',
        'price',
        'category_name',
    ]
class OrderAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'customer',
    ]

# Register your models here.
admin.site.register(Category)
admin.site.register(Products,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Customer)
admin.site.register(shippingAddress)