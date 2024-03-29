from django.db import models
from .customer import Customer

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    
    def __str__(self) -> str:
        return str(self.id)+" - "+(self.customer.name)
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
    def get_all_by_customer_id(id):
        return Order.objects.filter(customer__user__id=id).reverse()

    @staticmethod
    def get_customer_by_id(id):
        return Order.objects.get(customer__user__id=id)

    @staticmethod
    def get_panding_by_customer_id(id):
        return Order.objects.get(
            customer__user__id=id,
            complete=False)
