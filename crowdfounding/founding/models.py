from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
   
    title = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pictures = models.ImageField(upload_to='project_images/', blank=True, null=True)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @property
    def is_featured(self):
        return self.donations.count() > 10 or self.ratings.count() > 5

    def __str__(self):
        return self.title


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')  # Associate donation with user
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_donated = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments') 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
   
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
   
    rating = models.PositiveIntegerField(default=0)  # Range 1 to 5





