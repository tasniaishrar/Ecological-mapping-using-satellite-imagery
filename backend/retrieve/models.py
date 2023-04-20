from django.db import models

# Create your models here.
class Picture(models.Model):
    img_url = models.ImageField(upload_to='images/')
    