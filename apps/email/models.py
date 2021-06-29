from django.db import models

# Create your models here.
class Email(models.Model):
    name = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254)
    review = models.TextField(blank=True, null=True)