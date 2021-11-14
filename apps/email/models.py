from django.db import models

# Create your models here.
class Email(models.Model):
    name = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254)
    review = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/',  # lambda instance, filename: f"courses/{instance.pk}/avatars/{filename}",
        blank=True,
        null=True
    )