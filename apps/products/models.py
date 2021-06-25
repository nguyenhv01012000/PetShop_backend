from django.db import models

# Create your models here.
class Category(models.Model):
    cateName = models.CharField(max_length=140, default='SOME STRING')

class Product(models.Model):
    productName = models.TextField(blank=True, null=True)
    # category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    productSale = models.IntegerField(default=0)
    productSold = models.IntegerField(default=0)
    productDate = models.DateTimeField(auto_now=True)
    productPrice = models.IntegerField(default=0)
    productCate = models.TextField(blank=True, null=True)
    productColor = models.JSONField(null=True)
    productDes = models.TextField(blank=True, null=True)
    productVote = models.JSONField(null=True)
    productFeature = models.JSONField(null=True)
    productImg = models.ImageField(
        upload_to='images/',  # lambda instance, filename: f"courses/{instance.pk}/avatars/{filename}",
        blank=True,
        null=True
    )


