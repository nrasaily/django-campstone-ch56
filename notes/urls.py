from django.urls import path
from . import views


urlpatterns = [
  path('', views.NoteList.as_view(), name='note_list'),
  path('create/', views.NoteCreate.as_view(), name='note_create'),
]