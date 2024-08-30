
# from atexit import register
from .views import register
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('projectlist/', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    path('create-category/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'), 
<<<<<<< HEAD
    
=======
    path('categories/<slug:category_slug>/', views.category_projects, name='category_projects'),

>>>>>>> kHome
]