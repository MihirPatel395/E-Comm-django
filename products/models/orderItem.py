from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from .product import Products
from .order import Order
from .customer import Customer


class OrderItem(models.Model):
    product=models.ForeignKey(Products,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self) -> str:
        return self.product.name
    
    @property
    def get_total(self):
        return self.product.price*self.quantity

    @staticmethod
    def add_product_by_id(request,product_id,user_id):
        product=Products.get_product_by_id(product_id)

        try:
            order=Order.objects.get(customer__user__id=user_id,complete=False)
        except:
            user=User.objects.get(id=user_id)
            customer=Customer.objects.get(user__id=user_id)
            order=Order.objects.create(customer=customer)
        try:
            old_order=OrderItem.objects.get(order=order,product=product)
        except:
            old_order=''
        
        if old_order:
            messages.info(request,'Product is already in your cart')
            return True
            old_order.quantity+=1
            old_order.save()
        else:
            OrderItem.objects.create(order=order,product=product,quantity=1)
        
        
    @staticmethod
    def delete_product_by_id(product_id,user_id):
        try:
            product=Products.get_product_by_id(product_id)
            order=Order.objects.get(customer__user__id=user_id)
            OrderItem.objects.get(order=order,product=product).delete()
            return True
        except:
            return False