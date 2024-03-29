from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200, null=True,blank=True)
    email=models.EmailField(max_length=200, null=True,blank=True)
    img=models.ImageField(upload_to='profile/',null=True,blank=True)

    def __str__(self) -> str:
        return self.name

    def imgUrl(self):
        try:
            url=self.img.url
        except:
            url=''
        return url