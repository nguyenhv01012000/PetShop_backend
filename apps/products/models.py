from django.db import models

# Create your models here.
class Product(models.Model):
    productName = models.TextField(blank=True, null=True)
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


class Category(models.Model):
    cateName = models.TextField(blank=True, null=True)