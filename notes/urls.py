from django.urls import path
from . import views
from .views import NoteDelete, NoteUpdate, NoteCreate

urlpatterns = [
  path('', views.NoteList.as_view(), name='note_list'),
  path('create/', views.NoteCreate.as_view(), name='note_create'),
  path('update/<int:pk>/', NoteUpdate.as_view(), name='note_update'),
  path('delete/<int:pk>/', NoteDelete.as_view(), name='note_delete'),
]