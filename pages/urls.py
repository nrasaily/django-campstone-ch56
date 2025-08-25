from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name="root"),
    path("home/", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path('login/', auth_views.LoginView.as_view(template_name="pages/login.html"), name='login'),
    path("signup/", views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout" ),
    path("upload/", views.upload_document_view, name="upload"),
    path("success", views.success_view, name="success"),
    
]