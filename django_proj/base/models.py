from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    releaseYear = models.IntegerField(default = 2137)
    borrowed = models.BooleanField(default = False)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title) + ' ' + str(self.releaseYear)
    
    class Meta:
        ordering = ['-created']
    
class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null = True)
    startDate = models.DateField(auto_now_add = True)
    endDate = models.DateField(default = datetime.now().date() + timedelta(days=14))

    def __str__(self):
        return str(self.user.username) + '-' + str(self.endDate)