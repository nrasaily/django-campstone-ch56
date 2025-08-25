from django.urls import path
from .views import password_reset_request

from django.contrib.auth import views as auth_views

urlpatterns = [
  path("password_reset/", password_reset_request, name="password_reset_request"),
  path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
  path("reset/<uidb64>/<token>/",
  auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
  name="password_reset_confirm"),
  path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
  path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
  path('password_change/', 
  auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), 
  name='password_change'),
  path('password_change/done/', 
  auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
  name='password_change_done'),
]