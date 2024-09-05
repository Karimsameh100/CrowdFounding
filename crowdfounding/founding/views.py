from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from  django.db.models import  Avg
from .models import Project,Category,Rating
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    ratings = Rating.objects.values('project_id').annotate(total_rating=Avg('rating')).order_by('-total_rating')
    highest_rated_projects = Project.objects.filter(id__in=[rating['project_id'] for rating in ratings[:5]], is_active=True)
    latest_projects = Project.objects.all().order_by('-start_time')[:5]
    for project in latest_projects:
        project.avg_rating = project.ratings.all().aggregate(Avg('rating'))['rating__avg']
    # featured_projects = Project.objects.filter(is_featured=True).order_by('-start_time')[:5]
    categories = Category.objects.all()

    return render(request, 'founding/home.html', {
        'highest_rated_projects': highest_rated_projects,
        'latest_projects': latest_projects,
        'categories': categories,
    })


# def home(request):
#     return render(request,"founding/home.html")

def category_projects(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    projects = Project.objects.filter(category=category)
    return render(request, 'founding/category_projects.html', {'projects': projects})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Redirect to the category list or any other appropriate page
    else:
        form = CategoryForm()
    return render(request, 'founding/create_category.html', {'form': form})

@login_required
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

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.filter(category=project.category).exclude(pk=pk)[:5]
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'donate' in request.POST:
            # Handle donation
            amount = request.POST.get('amount')
            if amount and float(amount) > 0:
                Donation.objects.create(user=request.user, project=project, amount=amount)
                return redirect('project_detail', pk=pk)

        elif 'comment' in request.POST:
            # Handle comment submission
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.project = project
                comment.save()
                return redirect('project_detail', pk=pk)

    return render(request, 'founding/project_detail.html', {
        'project': project,
        'related_projects': related_projects,
        'comment_form': comment_form
    })







from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import RegistrationForm
# from django.contrib.auth.models import User








# from django.shortcuts import render, redirect
# from .forms import RegistrationForm
# from django.contrib.auth.models import User

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
           
#             user = User(
#                 first_name=form.cleaned_data['first_name'],
#                 last_name=form.cleaned_data['last_name'],
#                 email=form.cleaned_data['email'],
#                 username=form.cleaned_data['email']
#             )
#             user.set_password(form.cleaned_data['password'])
#             user.save()

           
#             return render(request, 'founding/registerform.html', {
#                 'form': form,
#                 'success': True
#             })
#     else:
#         form = RegistrationForm()

#     return render(request, 'founding/registerform.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import Profile
# from .utils import send_activation_email  # تأكد من أن وظيفة send_activation_email متاحة هنا

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
           
          
            user = User(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email'],
                is_active=False 
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = Profile(user=user)
            profile.save()

            send_activation_email(user, request)

        
            return render(request, 'founding/registerform.html', {
                'form': form,
                'success': True
            })
    else:
        form = RegistrationForm()

    return render(request, 'founding/registerform.html', {'form': form})

# ////////////////////////
from django.contrib.auth import authenticate, login as auth_login

from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            
           # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Log the user in
                auth_login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                return HttpResponse('Invalid login credentials.')  # Show error message if authentication fails
        else:
            return HttpResponse('Invalid form input.')  # Show error if form is not valid
    else:
        form = LoginForm()
    
    return render(request, 'founding/login.html', {'form': form})

           
              
    
    # -------------------------------------------------activation 
import hashlib
import random
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import Profile

def send_activation_email(user, request):
    token = hashlib.sha256(str(random.random()).encode()).hexdigest()
    profile = Profile.objects.get(user=user)
    profile.activation_token = token
    profile.activation_token_created_at = now()
    profile.save()

    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f'http://{current_site.domain}{activation_link}'

    message = render_to_string('founding/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })

    send_mail(mail_subject, message, 'noreply@yourdomain.com', [user.email])












from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from .models import Profile

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        profile = Profile.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Profile.DoesNotExist):
        user = None

    if user and profile.activation_token == token and not profile.is_token_expired():
        user.is_active = True
        user.save()
        profile.is_active = True
        profile.activation_token = None
        profile.save()
        return render(request, 'founding/activation_success.html')
    else:
        return render(request, 'founding/activation_failed.html')
