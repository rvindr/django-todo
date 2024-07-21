from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='todo')

    def __str__(self):
        return self.name
    
