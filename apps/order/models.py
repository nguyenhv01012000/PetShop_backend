from django.db import models

class Order(models.Model):
    orderAvatar = models.TextField(blank=True, null=True)
    orderName = models.TextField(blank=True, null=True)
    orderEmail = models.TextField(blank=True, null=True)
    orderPhone = models.TextField(blank=True, null=True)
    orderAddress = models.TextField(blank=True, null=True)
    orderTinh = models.TextField(blank=True, null=True)
    orderHuyen= models.TextField(blank=True, null=True)
    orderList= models.JSONField(null=True)
    orderTotal = models.IntegerField(default=0)
    orderPaymentMethod = models.TextField(blank=True, null=True)
    orderDate = models.DateTimeField(auto_now=True)

