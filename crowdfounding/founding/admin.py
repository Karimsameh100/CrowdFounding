from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Donation)
admin.site.register(Profile)