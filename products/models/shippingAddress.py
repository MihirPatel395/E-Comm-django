from django.db import models
from .order import Order
from .customer import Customer

class shippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=200, null=True,blank=True)
    city=models.CharField(max_length=200, null=True,blank=True)
    country=models.CharField(max_length=200, null=True,blank=True)
    pincode=models.CharField(max_length=200, null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address+" ("+str(self.order.id)+")"