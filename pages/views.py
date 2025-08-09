from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import TaxDocumentForm
from .models import Client

# Create your views here.

def home_view(request):
    return render(request, "pages/home.html")

def about_view(request):
    return render(request, "pages/about.html")

def contact_view(request):
    return render(request, 'pages/contact.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # or 'dashboard'
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {"form": form})

def logout_view(request):
    logout(request)
    return render(request, 'pages/logout.html') # shows the confimation screen

def upload_document_view(request):
    if request.method == 'POST':
        form = TaxDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False) # Don't save yet
            document.client = Client.objects.first() # choose real client
            return redirect('success')
    else:
        form = TaxDocumentForm()
    return render(request, 'upload_document.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')
