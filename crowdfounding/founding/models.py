from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    pictures = models.ImageField(upload_to='project_images/', blank=True, null=True)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_donated = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)  # Range 1 to 5


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    slug = models.SlugField(null=True , blank=True)
    img=models.ImageField(upload_to="profile_img")
    join_Date= models.DateTimeField(blank=True,default=datetime.datetime.now)
    country=models.CharField(blank=True,max_length=50)


def save(self , *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.user)
    super ( Profile , self).save (*args, **kwargs)
    
def _str_(self):
    return '%s' %(self.user)


##Signals...
def create_profile(sender , **kwargs):
    if kwargs ['created'] :
        user_profile = Profile.objects.create(user=kwargs['instance'])
        
post_save.connect(create_profile , sender=User)        