from django import forms
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'pictures', 'total_target', 'tags', 'start_time', 'end_time']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
