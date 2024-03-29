from django.db import models
from django.urls import reverse
from .category import Category


class Products(models.Model):
    category_name= models.ForeignKey(Category,on_delete=models.CASCADE)
    name= models.CharField(max_length=120, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    price= models.FloatField(help_text='in Indian Rupee Rs',blank=True, null=True)
    img=models.ImageField(upload_to='products/',null=True,blank=True)
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
    
    def imgUrl(self):
        try:
            url=self.img.url
        except:
            url=''
        return url

    @staticmethod
    def get_product_by_id(id):
        try:
            return Products.objects.get(id=id)
        except:
            return ''