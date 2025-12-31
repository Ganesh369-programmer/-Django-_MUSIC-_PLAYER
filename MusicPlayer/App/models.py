from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Song(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255 , blank=True)
    file = models.FileField(upload_to='music/')
    duration = models.IntegerField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
    

