from django.db import models

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Image_Binary(models.Model):
    image_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

