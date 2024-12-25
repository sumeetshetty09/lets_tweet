from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Tweet(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   text = models.TextField(max_length=255)
   photo = models.ImageField(upload_to='photos/', blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self): #it is useful for whenever we integrate this model in Admin, it will give us the demo/url from this class which can be used to see fields of the model/class which can be modified in admin page.
     return f'{self.user.username} - {self.text[:10]}'
