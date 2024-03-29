from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=80)
    description= models.CharField(max_length=250, blank=True, null=True)
    # img=models.ImageField(height_field=None, width_field=None, max_length=None,null=True,blank=True)
    create_at=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
            return self.name


class Products(models.Model):
    category_name= models.ForeignKey(Category,on_delete=models.CASCADE)
    name= models.CharField(max_length=120, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    price= models.FloatField(help_text='in Indian Rupee Rs',blank=True, null=True)
    # img=models.ImageField()
    create_at=models.DateField(auto_now_add=True,null=True,blank=True)

    class Meta:
        ordering=['-create_at']

    # to see name of field at admin
    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self):
         return reverse('product',kwargs={
              'pk':self.id,
         })

    @staticmethod
    def get_product_by_id(id):
        try:
            return Products.objects.get(id=id)
        except:
            return ''
    
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200, null=True,blank=True)
    email=models.EmailField(max_length=200, null=True,blank=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.customer.name
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @staticmethod
    def get_customer_by_id(id):
        return Order.objects.get(customer__user__id=id)
    
    
    

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
            order=Order.objects.get(customer__user__id=user_id)
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