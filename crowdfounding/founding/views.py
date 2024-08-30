from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ProjectForm,CategoryForm
from .models import *

# Create your views here.

def home(request):
    return render(request,"founding/home.html")



def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the category list or any other appropriate page
    else:
        form = CategoryForm()
    return render(request, 'founding/create_category.html', {'form': form})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Redirect to the list of projects after creation
    else:
        form = ProjectForm()
    categories = Category.objects.all()  # Fetch categories to render in the form
    return render(request, 'founding/create_project.html', {'form': form, 'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'founding/category_list.html', {'categories': categories})

def project_list(request):
    projects = Project.objects.filter(is_active=True)
    return render(request, 'founding/project_list.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'founding/project_detail.html', {'project': project})
