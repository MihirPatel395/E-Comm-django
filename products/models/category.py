from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=80)
    description= models.CharField(max_length=250, blank=True, null=True)
    # img=models.ImageField(height_field=None, width_field=None, max_length=None,null=True,blank=True)
    create_at=models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self) -> str:
            return self.name
