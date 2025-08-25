from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import TaxDocumentForm
from .models import Client
from django.core.mail import send_mail, EmailMessage
from .forms import ContactForm
from django.conf import settings
from django.http import Http404, HttpResponse


# Create your views here.

def home_view(request):
    return render(request, "pages/home.html")

def about_view(request):
    return render(request, "pages/about.html")

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # 1) email to admil notification
            owner_subject = f"[Paarijat Contact] Message from {name}"
            owner_body = (
                f"New contact submission\n\n"
                f"Name : {name}\n"
                f"Email: {email}\n\n"
                f"Message: \n{message}\n"
            )
            # Use your authenticated sender; add reply-To so you can reply to the user
            owner_email = EmailMessage(
                subject=owner_subject,
                body=owner_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=getattr(settings, "CONTACT_RECIPIENTS", [settings.DEFAULT_FROM_EMAIL]),
                headers={"Reply-To": email},
            )
            owner_email.send(fail_silently=False)

            #--2) Auto-reply to USER -----
            user_subject = "Thanks for contacting Paarijat Tax Service"
            user_body = (
                f"Hi {name},\n\n"
                "Thanks for reaching out to Paarijat Tax Service. "
                "We've recieved your message and will get back to you Shortly.\n\n"
                "f{message}\n\n"
                "Regards,\nPaarijat Tax Service\n771 N Plymouth Ave, Rochester, NY 14608\n+1 (585) 555-1234"
            )
            user_email_msg = EmailMessage(
                subject=user_subject,
                body=user_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            try:
                owner_email.send(fail_silently=False)
                user_email_msg.send(fail_silently=False)
                messages.success(request, "thanks! Your nessage has been sent.")
                return redirect("contact") # or a 'success' page
            except Exception as exc:
              # Log exc in real apps
              messages.error(request, "Sorrry, we could not send your message right now. Please try again later.")
        else: 
            messages.error(request, "Please fix the errors below.")
    else: 
        form = ContactForm()
        
    return render(request, "pages/contact.html", {"form": form})



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

