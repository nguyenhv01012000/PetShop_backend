from django.db import models

class News(models.Model):
    newImg = models.ImageField(
        upload_to='images/',  # lambda instance, filename: f"courses/{instance.pk}/avatars/{filename}",
        blank=True,
        null=True
    )
    newCate = models.TextField(blank=True, null=True)
    newTitle = models.TextField(blank=True, null=True)
    newContent = models.TextField(blank=True, null=True)
    newView = models.IntegerField(default=0)
    newTime = models.DateTimeField(auto_now=True)

